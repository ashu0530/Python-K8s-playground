from flask import Flask, request, redirect, render_template, render_template_string, url_for, session, jsonify
import os
from kubernetes import client, config
from flask_session import Session
import uuid
import redis
from datetime import timedelta, datetime
from wtforms import Form, StringField, PasswordField, validators
from auth import User, register, login
from flask_login import login_required, current_user
from auth import auth_blueprint, User, db, login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # Change this to your secret key
app.register_blueprint(auth_blueprint)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

login_manager.init_app(app)


custom_kubeconfig_path = "/root/.kube/config"
config.load_kube_config(config_file=custom_kubeconfig_path)

api_instance = client.CoreV1Api()
ingress_api = client.NetworkingV1Api()

redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)

target_namespace = "ashutosh"


class UserForm(Form):
    pod_name = StringField('Pod Name', [validators.DataRequired()])

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_nginx_pod():
#    if 'email' not in session:
#        return redirect('/login')

    form = UserForm(request.form)

    if request.method == 'POST' and form.validate():
        pod_name = form.pod_name.data
        session_id = str(uuid.uuid4())

        if session_id and redis_client.exists(session_id):
            return "You already have an active session (Nginx pod)."

        # Fetch user information from database
        user = User.query.filter_by(email=current_user.email).first()
        if not user:
            return "User not found", 404

        unique_pod_name = f"nginx-pod-{session_id}"
        unique_service_name = f"nginx-service-{session_id}"
        ingress_host = f"{session_id}.youringressurl"

        creation_timestamp = datetime.now().isoformat()
        redis_data = {"pod_name": pod_name, "creation_timestamp": creation_timestamp}
        redis_data = {str(key): str(value) for key, value in redis_data.items()}  # Convert keys and values to strings
        try:
            redis_client.hset(session_id, mapping=redis_data)
            app.logger.info(f"Saved data to Redis: {redis_data}")
        except Exception as e:
            app.logger.error(f"Error saving data to Redis: {e}")

        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": unique_pod_name,
                "labels": {"app": "nginx", "session_id": session_id},
                "namespace": target_namespace
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx:latest"
                    }
                ]
            }
        }
        api_instance.create_namespaced_pod(namespace=target_namespace, body=pod_manifest)

        service_manifest = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": unique_service_name,
                "namespace": target_namespace,
                "labels": {"app": "nginx", "session_id": session_id}
            },
            "spec": {
                "ports": [
                    {
                        "port": 80,
                        "targetPort": 80
                    }
                ],
                "selector": {"app": "nginx", "session_id": session_id}
            }
        }
        api_instance.create_namespaced_service(namespace=target_namespace, body=service_manifest)

        ingress_manifest = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": f"nginx-ingress-{session_id}",
                "namespace": target_namespace
            },
            "spec": {
                "ingressClassName": "nginx",
                "rules": [
                    {
                        "host": ingress_host,
                        "http": {
                            "paths": [
                                {
                                    "backend": {
                                        "service": {
                                            "name": unique_service_name,
                                            "port": {"number": 80}
                                        }
                                    },
                                    "path": "/",
                                    "pathType": "Prefix"
                                }
                            ]
                        }
                    }
                ]
            }
        }
        ingress_api.create_namespaced_ingress(namespace=target_namespace, body=ingress_manifest)

        ingress_url = f"http://{ingress_host}"

        return redirect(ingress_url)

    return render_template('create.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    session_id = request.form.get('session_id')
    if session_id is None:
        return "Session ID is required to logout.", 400

    pod_name = redis_client.hget(session_id, 'pod_name')
    if pod_name:
        pods = api_instance.list_namespaced_pod(namespace=target_namespace, label_selector=f"session_id={session_id}")

        for pod in pods.items:
            api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace=target_namespace)

        service_name = f"nginx-service-{session_id}"
        api_instance.delete_namespaced_service(name=service_name, namespace=target_namespace)

        ingress_name = f"nginx-ingress-{session_id}"
        ingress_api.delete_namespaced_ingress(name=ingress_name, namespace=target_namespace)

        redis_client.delete(session_id)

        return jsonify({"message": "Logged out and deleted pods, services, and Ingress.", "pod_name": pod_name.decode()}), 200
    else:
        return "Session ID not found in Redis.", 404
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

