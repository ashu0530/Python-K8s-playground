from kubernetes import client 
import os

configuration = client.Configuration()
configuration.api_key['authorization'] = os.getenv("KIND_TOKEN", None)  

configuration.api_key_prefix['authorization'] = 'Bearer'
configuration.verify_ssl = False

configuration.host = "https://localhost:6443"

api_client = client.ApiClient(configuration)
v1 = client.CoreV1Api(api_client)

fetch = v1.list_namespaced_pod(namespace="ashu", watch=False)
for pod in fetch.items:
    print(f"Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace} IP: {pod.status.pod_ip}")