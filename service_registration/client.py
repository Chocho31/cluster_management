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

    def get_container_ips(self, container):
        ips = []
        cont = self.get_container(container)
        networks = cont.attrs['NetworkSettings']['Networks']

        for key in networks.keys():
            cont_ip = networks[key]["IPAddress"]

            if cont_ip != '':
                ips.append(cont_ip)

        return ips

    def get_container_networks(self, container):
        cont = self.get_container(container)
        attrs = cont.attrs
        networks = attrs['NetworkSettings']['Networks'].keys()
        return list(networks)

    def get_container_IP(self, container, network):
        cont = self.get_container(container)
        attrs = cont.attrs
        return attrs['NetworkSettings']['Networks'][network]['IPAddress']

    def get_container_exposed_port(self, container):
        cont = self.get_container(container)
        attrs = cont.attrs
        exposed_ports = attrs['Config'].get('ExposedPorts', None)
        if exposed_ports:
            port_with_protocol = list(attrs['Config']['ExposedPorts'].keys())[0]
            return int(port_with_protocol[:-4])

        return None

    def get_container_stats(self, container):
        return self.get_container(container).stats(stream=False)

    def get_events(self):
        return self.client.events(decode=True)
