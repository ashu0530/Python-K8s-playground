from kubernetes import client, config

def create_nginx_pod():
    config.load_kube_config()
    api_instance = client.CoreV1Api()

    #the Pod manifest
    pod_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": "nginx-pod"
        },
        "spec": {
            "containers": [{
                "name": "nginx-container",
                "image": "nginx",
                "ports": [{
                    "containerPort": 80
                }]
            }]
        }
    }

    try:
        # Create the Pod
        api_response = api_instance.create_namespaced_pod(
            body=pod_manifest,
            namespace="ashu"
        )
        print("Pod created successfully.")
    except Exception as e:
        print(f"Failed to create Pod: {e}")

if __name__ == "__main__":
    create_nginx_pod()
