from influxdb import InfluxDBClient
from datetime import datetime, timedelta


class InfluxAggregator:
    def __init__(self, config):
        self.db_connection = InfluxDBClient(**config)
        self.service_metrics_handler = {
            'cpu': self.get_service_cpu,
            'memory': self.get_service_memory
        }
        self.container_metrics_handler = {
            'cpu': self.get_container_cpu,
            'memory': self.get_container_memory
        }

    def format_date(self, date):
        # could also use date.strftime('%Y-%m-%dT%H:%M:%SZ')
        return date.isoformat('T') + 'Z'

    def get_service_metric(self, metric, service):
        metric_handler = self.service_metrics_handler[metric]
        return metric_handler(service=service)

    def get_container_metric(self, metric, container_id):
        metric_handler = self.container_metrics_handler[metric]
        return metric_handler(cont_id=container_id)

    def get_service_cpu(self, service, period=30):
        date = datetime.utcnow() - timedelta(seconds=period)
        timestamp = self.format_date(date)
        print(timestamp)

        query = (
            "select mean(percentage) "
            "from cpu_usage "
            "where service = $service and time >= $timestamp"
        )
        bind_params = {
            'service': service,
            'timestamp': timestamp
        }

        result = self.db_connection.query(
            query=query, bind_params=bind_params)
        print(result)

        gen = result.get_points(measurement='cpu_usage')
        return next(gen)['mean']

    def get_service_memory(self, service, period=30):
        date = datetime.now() - timedelta(seconds=period)
        timestamp = self.convert_to_utc(date)

        query = (
            "select mean(percentage) "
            "from memory_usage "
            "where service = $service and time >= $timestamp"
        )
        bind_params = {
            'service': service,
            'timestamp': timestamp
        }

        result = self.db_connection.query(
            query=query, bind_params=bind_params)

        gen = result.get_points(measurement='memory_usage')
        return next(gen)['mean']

    def get_container_cpu(self, cont_id, period=30):
        date = datetime.now() - timedelta(seconds=period)
        timestamp = self.convert_to_utc(date)

        query = (
            "select mean(percentage) "
            "from cpu_usage "
            "where container_id = $id and time >= $timestamp"
        )
        bind_params = {
            'id': cont_id,
            'timestamp': timestamp
        }

        result = self.db_connection.query(
            query=query, bind_params=bind_params)

        gen = result.get_points(measurement='cpu_usage')
        return next(gen)['mean']

    def get_container_memory(self, cont_id, period=30):
        date = datetime.now() - timedelta(seconds=period)
        timestamp = self.convert_to_utc(date)

        query = (
            "select mean(percentage) "
            "from memory_usage "
            "where container_id = $id and time >= $timestamp"
        )
        bind_params = {
            'id': cont_id,
            'timestamp': timestamp
        }

        result = self.db_connection.query(
            query=query, bind_params=bind_params)

        gen = result.get_points(measurement='memory_usage')
        return next(gen)['mean']

    def get_container_blockio(self, cont_id):
        query = (
            "select read_bytes, write_bytes "
            "from blockio "
            "where container_id = $id"
        )
        bind_params = {
            'id': cont_id
        }

        result = self.db_connection.query(
            query=query, bind_params=bind_params)

        gen = result.get_points(measurement='blockio')
        bytes = next(gen)
        return bytes['read_bytes'], bytes['write_bytes']

    def __del__(self):
        self.db_connection.close()
