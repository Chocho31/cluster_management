from datetime import datetime, timedelta
from errors import EmptyResultSetException


class Scaler:
    def __init__(self, config, docker_client, scheduler, metrics_aggregator):
        self.docker_client = docker_client
        self.scheduler = scheduler
        self.metrics_aggregator = metrics_aggregator
        self.interval = config.get('poll_interval', 30)
        self.upscale_delay = config.get('upscale_delay', 180)
        self.downscale_delay = config.get('downscale_delay', 300)
        self.rules = config['rules']

    def start(self):
        # schedule check_metrics for each service in the rules for the scaler
        for rule in self.rules:
            service = rule['service']
            min_instances = rule['min_instances']
            max_instances = rule['max_instances']
            observed_metrics = rule['metrics']

            kwargs = {
                'service': service,
                'min_instances': min_instances,
                'max_instances': max_instances,
                'metrics': observed_metrics
            }

            self.scheduler.add_job(
                func=self.check_metrics,
                kwargs=kwargs,
                id=service,
                trigger='interval',
                seconds=self.interval,
                next_run_time=datetime.now()
            )

        self.scheduler.start()

    def check_metrics(self, service, min_instances, max_instances, metrics):
        # extract metrics for the service
        # scale up if heavily loaded, scale down if load is low

        for metric in metrics:
            try:
                metric_value = self.metrics_aggregator.get_service_metric(
                    metric['name'], service)
            except EmptyResultSetException:
                print("Metric value is empty")
                continue

            scale_up_threshold = metric['threshold']['scale_up']
            scale_down_threshold = metric['threshold']['scale_down']

            if metric_value >= scale_up_threshold:
                self.scale_up(service, max_instances)

                # wait until metrics stabilize
                # reschedule metrics checks to run after a period of time
                self.scheduler.modify_job(
                    job_id=service,
                    next_run_time=datetime.now() + timedelta(seconds=self.upscale_delay)
                )

                break

            elif metric_value <= scale_down_threshold:
                self.scale_down(service, min_instances)

                # avoid autoscaler trashing
                # reschedule metrics checks to run after a period of time
                self.scheduler.modify_job(
                    job_id=service,
                    next_run_time=datetime.now() + timedelta(seconds=self.downscale_delay)
                )

                break

    def scale_up(self, service, max_instances):
        # get current number of replicas and add 1 more instance
        # if number of maximum instances is not reached
        current_replicas = self.docker_client.get_replica_count(service)

        if current_replicas < max_instances:
            self.docker_client.scale_service(service, current_replicas + 1)

    def scale_down(self, service, min_instances):
        # get current number of replicas and remove 1 of the instances
        # if number of minimum instances is not reached
        current_replicas = self.docker_client.get_replica_count(service)

        if current_replicas > min_instances:
            self.docker_client.scale_service(service, current_replicas - 1)
