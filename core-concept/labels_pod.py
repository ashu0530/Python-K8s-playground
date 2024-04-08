#import kubernetes
#help(kubernetes) want to take reference of packages inside kubernetes uncomment it


from kubernetes import client, config
#help(client.CoreV1Api)



#create a pod function with labels
def create_pod():
    
    #Connection with k8s cluster with default context

    config.load_kube_config()
    api = client.CoreV1Api()
    
    nginx_container = client.V1Container(
        name="nginx-container",
        image="nginx",
        ports=[client.V1ContainerPort(container_port=80)]
        
    )

    labels= {"app": "nginx-ashu"}

    metadata=client.V1ObjectMeta(name="nginx",labels=labels)

      # create a v1podspec object to define pod specification
    pod_spec = client.V1PodSpec(containers=[nginx_container])

    pod = client.V1Pod(metadata=metadata, spec=pod_spec)


    
    #try and exceptional method here for creating the pod
    try:
        api_result = api.create_namespaced_pod(
            body=pod,
            namespace="ashu"

        )
        print("pod successfully created.")
    except Exception as y:
        print(f"failed to create pod: {y}")



create_pod()

