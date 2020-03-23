from apscheduler.schedulers.blocking import BlockingScheduler
from store import InfluxStore
from collector import Collector
from client import DockerSDKClient
import yaml

if __name__ == "__main__":
    with open("config.yml", 'r') as conf_file:
        config = yaml.safe_load(conf_file)

        docker_client = DockerSDKClient()
        scheduler = BlockingScheduler()
        metrics_store = InfluxStore(config['metrics_store'])
        interval = config.get('poll_interval', 30)

        collector = Collector(
            docker_client, scheduler, metrics_store, interval)

    collector.start()
