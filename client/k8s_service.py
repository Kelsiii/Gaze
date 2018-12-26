from kubernetes import client, config

class K8SClient(object):
    def __init__(self):
        # it works only if this script is run by K8s as a POD
        config.load_incluster_config()
        self.core_v1 = client.CoreV1Api()
        self.extensions_v1beta1 = client.ExtensionsV1beta1Api()

    def get_all_pods(self):
        ret = self.core_v1.list_pod_for_all_namespaces(watch=False,timeout_seconds=30)
        pods = []
        for i in ret.items:
            #print("%s\t%s\t%s" %
            #    (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
            if i.metadata.namespace=="default":
                #print(i)
                pods.append({
                    "name": i.metadata.name,
                    "image": i.spec.containers[0].image,
                    "phase": i.status.phase,
                    "ip": i.status.pod_ip
                })
        return pods

    def delete_pod(self, pod_name):
        try:
            api_response = self.core_v1.delete_namespaced_pod(
                namespace="default",
                name = pod_name,
                body = client.V1DeleteOptions()
            )
            return True, str(api_response.status)
        except Exception as e:
            return False, str(e)

    def create_deployment(self,deployment):
        # Create deployement
        api_response = self.extensions_v1beta1.create_namespaced_deployment(
            body=deployment,
            namespace="default")
        print("Deployment created. status='%s'" % str(api_response.status))

    def create_pod(self,pod):
        try:
            api_response = self.core_v1.create_namespaced_pod(
                namespace="default", 
                body=pod)
            return True, str(api_response.status)
        except Exception as e:
            return False, str(e)

    def create_pod_object(self, name, image, key, env, port=5001):
        image_env = []
        for k in env:
            value = env[k]
            image_env.append(client.V1EnvVar(name=k,value=value))
        container = client.V1Container(
            name=key,
            image=image,
            env=image_env,
            ports=[client.V1ContainerPort(container_port=port)]
        )
        spec = client.V1PodSpec(
            containers=[container]
        )
        metadata = client.V1ObjectMeta(
            name=name.replace("_","-"),
            labels={
                "name":name.replace("_","-")
            }
        )
        pod = client.V1Pod(
            api_version="v1",
            kind="Pod",
            metadata=metadata,
            spec=spec
        )
        return pod

'''
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "dockertest"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=3,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)
    
    return deployment

if __name__ == '__main__':
    config.load_kube_config(".\config")
    v1 = client.CoreV1Api()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()

    print_all_nodes(v1)

    #config.load_incluster_config()

    api_instance = client.CoreV1Api()
    pod = create_pod_object()
    create_pod(api_instance, pod)
'''