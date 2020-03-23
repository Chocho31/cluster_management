import json


class Registrator:
    def __init__(self, docker_client, registry_client):
        self.docker_client = docker_client
        self.registry_client = registry_client

    def start(self):
        self.sync()

        networks = []

        for event in self.docker_client.get_events():
            print("==> event <==")
            print(json.dumps(event, indent=2))
            print("==> end <==")

            if event["Type"] == "network":
                network = event["Actor"]["Attributes"]["name"]

                if event["Action"] == "connect":
                    networks.append(network)

                elif event["Action"] == "disconnect":
                    self.deregister(container, network)

            if event["Type"] == "container":
                if event["status"] == "start":
                    container = self.docker_client.get_container(event["id"])
                    
                    for network in networks:
                        self.register(container, network)

                    networks = []

                elif event["status"] == "stop":
                    container = self.docker_client.get_container(event["id"])
                    self.deregister(container)

    def register(self, container, network):
        # write container information in service registry
        # print(json.dumps(container.attrs, indent=2))

        cont_id = container.id
        labels = container.labels
        status = container.status
        print(labels)

        node_id = labels.get("com.docker.swarm.node.id", None)
        service = labels.get("com.docker.swarm.service.name", None)
        ip_addr = self.docker_client.get_container_IP(cont_id, network)
        port = self.docker_client.get_container_exposed_port(cont_id)

        print(cont_id, node_id, service, ip_addr, port, status)
        self.registry_client.add(
            cont_id, node_id, service, ip_addr, port, status)

        # perform error handling

    def deregister(self, container, network=None):
        # delete container information in service registry
        print(json.dumps(container.attrs, indent=2))

        if network:
            cont_ip = self.docker_client.get_container_IP(container.id, network)

        self.registry_client.remove(container.id, cont_ip)

        # perform error handling

    def sync(self):
        # if services exist before registrator is run -> perform registration
        all_containers = self.docker_client.get_containers()

        for container in all_containers:
            networks = container.attrs["NetworkSettings"]["Networks"].keys()
                
            for network in networks:
                self.register(container, network)
