from kubernetes import config, client
from kubernetes.client.rest import ApiException



def allowedIngressController(ns,target_ns):
    ingressControllerNginx=client.V1NetworkPolicy(
    metadata=client.V1ObjectMeta(name=f"allowed-ingress-from-{target_ns}"),
    spec=client.V1NetworkPolicySpec(
        policy_types=["Ingress"],
        pod_selector=client.V1LabelSelector(match_labels={}),
        ingress=[client.V1NetworkPolicyIngressRule(_from=[client.V1NetworkPolicyPeer(namespace_selector=client.V1LabelSelector(match_labels={'name': target_ns}))])],
    )
    )

    netpol = client.NetworkingV1Api()
    try:
        netpol.create_namespaced_network_policy(namespace=ns,body=ingressControllerNginx)
        print(f"Nginx Controller network policy applied to ns: {ns}")
    
    except client.exceptions.ApiException as e:
        print(f"Failed to apply network policy to ns {ns}: {e}")
    







def main():
    config.load_kube_config()
    ns = "ashu"
    target_ns_input = input("Enter values of ns separated by commas: ")
    target_ns_split= target_ns_input.split(',')

    
    for i in target_ns_split:
        allowedIngressController(ns.strip(),i.strip())


if __name__ == '__main__':
    main()
