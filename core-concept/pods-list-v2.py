from kubernetes import client 
import os

configuration = client.Configuration()
configuration.api_key['authorization'] = os.getenv("KIND_TOKEN", None)  

configuration.api_key_prefix['authorization'] = 'Bearer'
configuration.verify_ssl = True

#Path to the CA certificate file used by the Kubernetes API server
ca_cert_path = "/etc/kubernetes/pki/ca.crt"  # Replace with the actual path
configuration.ssl_ca_cert = ca_cert_path

configuration.host = "https://localhost:6443"  #use right hostname of kubernetes control-plane #hostnamectl command
api_client = client.ApiClient(configuration)
v1 = client.CoreV1Api(api_client)

fetch = v1.list_namespaced_pod(namespace="ashu", watch=False)
for pod in fetch.items:
    print(f"Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace} IP: {pod.status.pod_ip}")