from apscheduler.schedulers.blocking import BlockingScheduler
from aggregator import InfluxAggregator
from client import DockerSDKClient
from scaler import Scaler
import yaml

if __name__ == "__main__":
    with open("config.yml", 'r') as conf_file:
        config = yaml.safe_load(conf_file)
        print(config)

        docker_client = DockerSDKClient()
        scheduler = BlockingScheduler()
        metrics_aggregator = InfluxAggregator(config['metrics_store'])

        autoscaler = Scaler(config, docker_client,
                            scheduler, metrics_aggregator)

    autoscaler.start()
