#Created python application using k8s client library which can create the deployment with 5 replicas and its associated service.

#Module used :-
#V1Container  --> For creating Container configuration
#V1ContainerPort --> For port definition of container
#V1ResourceRequirements --> For configuring the resource requirements for containers
#V1SecurityContext -->  For defining security context of container
#V1Probe --> Liveness and readiness configuration module
#V1TCPSocketAction  --> For TCP socket in liveness and readiness
#V1PodTemplateSpec --> Pod Template section module
#V1ObjectMeta --> For metadata of any template or resources
#V1PodSpec --> Pod specification , taken from container spec
#V1Deployment --> Deployment module
#V1DeploymentSpec --> Deployment module specification where we define replicas, strategy etc
#V1LabelSelector  --> for labels and selectors 
#V1DeploymentStrategy --> Module for Deployment strategy like Recreate or rolling updates
#V1RollingUpdateDeployment  --> Rolling update strategy spec we define in this module
#V1Service --> Service module
#V1ServiceSpec --> Service specification module where we define port,selectors etc
#V1ServicePort --> For Service ports like target, nodeport etc



from kubernetes import client, config   
def main():
    
    config.load_kube_config()   #to connect with cluster on default location
    api_instance=client.AppsV1Api()   #for Apps/v1 resources
    api_svc=client.CoreV1Api()  #for V1 resources


  #container configurations
    container=client.V1Container(image="dockerproxy.repos.tech.orange/library/nginx",name="nginx", ports=[client.V1ContainerPort(protocol="TCP", container_port=80)], 
#            restart_policy="Always",
            resources=client.V1ResourceRequirements
            (requests={"cpu":"100m",
                       "memory":"200Mi"},
            limits  = {"cpu":"500m",
                       "memory":"500Mi"}),
            command=["/bin/sh"],
            args=["-c", "echo 'Hello World' > /usr/share/nginx/html/index.html && exec nginx -g 'daemon off;'" ],
            security_context=client.V1SecurityContext(allow_privilege_escalation=False),
            image_pull_policy="Never",
            liveness_probe=client.V1Probe(
                                initial_delay_seconds=3,
                                period_seconds=3,
                                tcp_socket=client.V1TCPSocketAction(port=80)),
                                readiness_probe=client.V1Probe(initial_delay_seconds=3,period_seconds=3,
                                tcp_socket=client.V1TCPSocketAction(port=80)))
  #pod template configurations
    pod_template=client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"env":"dev"}),spec=client.V1PodSpec(containers=[container]))
  #Deployment configurations
    deployment=client.V1Deployment(
            metadata=client.V1ObjectMeta(name="nginx",labels={"env":"dev"}),
            spec=client.V1DeploymentSpec(
                  replicas=5,
                  selector=client.V1LabelSelector(
                    match_labels={"env":"dev"}
                   ),
            strategy=client.V1DeploymentStrategy(
                    rolling_update=client.V1RollingUpdateDeployment(
                        max_surge="50%",
                        max_unavailable="50%"
                    )
            ),
            template=pod_template
            )
    )

  #Service configuration
    service=client.V1Service(metadata=client.V1ObjectMeta(name="nginx-svc",namespace="ashu",labels={"env":"dev"}),
                             spec=client.V1ServiceSpec(
                                selector={"env":"dev"},
                                type="NodePort",
                                ports=[client.V1ServicePort(target_port=80,node_port=31211,protocol="TCP",name="nginx",port=80)],                         )
                             )
#Exception handling case
    try:
        api_instance.create_namespaced_deployment(namespace="ashu",body=deployment)
        print("Deploy is created")
    except:
        print("Deploy is not created")

    try:
        api_svc.create_namespaced_service(namespace="ashu",body=service)
        print("svc is created")
    except:
        print("svc is not created")


if __name__ == "__main__":
    main()
