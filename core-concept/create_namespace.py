from kubernetes import client, config
from kubernetes.client.rest import ApiException

def createNS(name):
    
    v1=client.CoreV1Api()   
    ns = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
    try:
        v1.create_namespace(ns)
        print(f"Successfully created namespace '{name}' .")
    except ApiException as e:
        if e.status == 409:
            print(f"Namespace '{name}' already exists.")
        else:
            print(f"Exception when creating namespace: {e}")
        
    #To delete namespace      
        v1.delete_namespace(name=name, body=client.V1DeleteOptions())
                

def main():
    config.load_kube_config()  #load default kubeconfig file
    name="ashu-test"
    createNS(name)

if __name__ == "__main__":
    main()
