from kubernetes import client, config

# Specify the path to your custom kubeconfig file
#kubeconfig_path = "/path/to/your/kubeconfig.yaml"

# Load kubeconfig from the specified path and set it as the active configuration
#config.load_kube_config(config_file=kubeconfig_path)

config.load_kube_config()
v1 = client.CoreV1Api()
fetch = v1.list_namespaced_pod(namespace="ashu", watch=False)
for pod in fetch.items:
    print(f"Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace} IP: {pod.status.pod_ip}")
