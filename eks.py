from kubernetes import client, config
config.load_kube_config()
api_client = client.ApiClient()

deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="local_monitor"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "local_monitor"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "local_monitor"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="local_monitor_container",
                        image="682454692479.dkr.ecr.us-east-1.amazonaws.com/py_monitoring_app:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="monitoring-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "local_monitor"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)
