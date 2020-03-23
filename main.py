import json
import docker

client = docker.from_env()

container = client.containers.list()[0]
stats = container.stats(stream=False)
print(json.dumps(stats, indent=2))
