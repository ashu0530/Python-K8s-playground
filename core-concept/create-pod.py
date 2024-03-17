from kubernetes import client, config

def create_nginx_pod():
    config.load_kube_config()
    api_instance = client.CoreV1Api()
 
    # Create a V1Container object for the Nginx container
    nginx_container = client.V1Container(
        name="nginx-container",
        image="nginx",
        ports=[client.V1ContainerPort(container_port=80)]
    )

    # Create a V1PodSpec object to define the Pod specification
    pod_spec = client.V1PodSpec(
        containers=[nginx_container]
    )

    # Create a V1Pod object to define the Pod
    pod = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(name="nginx-pod"),
        spec=pod_spec
    )

    try:
        # Create the Pod
        api_response = api_instance.create_namespaced_pod(
            body=pod,
            namespace="default"
        )
        print("Pod created successfully.")
    except Exception as e:
        print(f"Failed to create Pod: {e}")

if __name__ == "__main__":
    create_nginx_pod()  ##run the function


