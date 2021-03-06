import docker


class DockerSDKClient:
    def __init__(self, client=None):
        self.client = client or docker.from_env()

    def get_services(self):
        return self.client.services.list()

    def get_service(self, service):
        return self.client.services.list(filters=dict(name=service))[0]

    def get_replica_count(self, service):
        service = self.get_service(service)
        return service.attrs['Spec']['Mode']['Replicated']['Replicas']

    def scale_service(self, service, replicas):
        return self.get_service(service).scale(replicas)

    def get_containers(self):
        return self.client.containers.list()

    def get_container(self, container):
        return self.client.containers.get(container)

    def get_container_IP(self, container, network):
        cont = self.get_container(container)
        attrs = cont.attrs
        return attrs['NetworkSettings']['Networks'][network]['IPAddress']

    def get_container_exposed_port(self, container):
        cont = self.get_container(container)
        attrs = cont.attrs
        port_with_protocol = list(attrs['Config']['ExposedPorts'].keys())[0]
        return int(port_with_protocol[:-4])

    def get_container_stats(self, container):
        return self.get_container(container).stats(stream=False)

    def get_cpu_stats(self, container):
        return self.get_container_stats(container)['cpu_stats']

    def get_precpu_stats(self, container):
        return self.get_container_stats(container)['precpu_stats']

    def get_memory_stats(self, container):
        return self.get_container_stats(container)['memory_stats']

    def get_blockio_stats(self, container):
        return self.get_container_stats(container)['blkio_stats']

    def get_events(self):
        return self.client.events(decode=True)
