import os
from kubernetes import client, config

def apply_default_network_policy(namespace):
    network_policy = client.V1NetworkPolicy(
        metadata=client.V1ObjectMeta(name="default-deny"),
        spec=client.V1NetworkPolicySpec(
            pod_selector=client.V1LabelSelector(match_labels={}),
            policy_types=["Ingress", "Egress"]
        )
    )
    
    netpol_v1 = client.NetworkingV1Api()
    try:
        netpol_v1.create_namespaced_network_policy(namespace=namespace, body=network_policy)
        print(f"Default network policy applied to namespace: {namespace}")
    
    except client.exceptions.ApiException as e:
        print(f"Failed to apply network policy to namespace {namespace}: {e}")

def allow_namespace_communication(current_ns, target_ns):
    # Allow ingress from target_ns to current_ns

    ingress_policy = client.V1NetworkPolicy(
        metadata=client.V1ObjectMeta(name="allow-ingress-from-target"),
        spec=client.V1NetworkPolicySpec(
            pod_selector=client.V1LabelSelector(match_labels={}),
            policy_types=["Ingress"],
            ingress=[client.V1NetworkPolicyIngressRule(
                _from=[client.V1NetworkPolicyPeer(
                    namespace_selector=client.V1LabelSelector(
                        match_labels={"name": target_ns}
                    )
                )]
            )]
        )
    )

    # Allow egress from current_ns to target_ns
    egress_policy = client.V1NetworkPolicy(
        metadata=client.V1ObjectMeta(name="allow-egress-to-target"),
        spec=client.V1NetworkPolicySpec(
            pod_selector=client.V1LabelSelector(match_labels={}),
            policy_types=["Egress"],
            egress=[client.V1NetworkPolicyEgressRule(
                to=[client.V1NetworkPolicyPeer(
                    namespace_selector=client.V1LabelSelector(
                        match_labels={"name": target_ns}
                    )
                )]
            )]
        )
    )

    netpol_v1 = client.NetworkingV1Api()
    try:
        netpol_v1.create_namespaced_network_policy(namespace=current_ns, body=ingress_policy)
        print(f"Ingress policy allowing traffic from {target_ns} to {current_ns} applied.")
    except client.exceptions.ApiException as e:
        print(f"Failed to apply ingress policy from {target_ns} to {current_ns}: {e}")

    try:
        netpol_v1.create_namespaced_network_policy(namespace=current_ns, body=egress_policy)
        print(f"Egress policy allowing traffic from {current_ns} to {target_ns} applied.")
    except client.exceptions.ApiException as e:
        print(f"Failed to apply egress policy from {current_ns} to {target_ns}: {e}")

def main():
    kubeconfig_path = os.getenv('KUBECONFIG', 'kubeconfig.yaml')
    config.load_kube_config(config_file=kubeconfig_path)

    current_ns = os.getenv('CURRENT_NS')
    target_ns = os.getenv('TARGET_NS')

    if not current_ns or not target_ns:
        print("Both CURRENT_NS and TARGET_NS environment variables must be set.")
        return
    #Apply both function
    apply_default_network_policy(current_ns)
    allow_namespace_communication(current_ns, target_ns)   

if __name__ == '__main__':
    main()
