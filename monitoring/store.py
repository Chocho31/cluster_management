from influxdb import InfluxDBClient


class InfluxStore:
    def __init__(self, config):
        self.db_connection = InfluxDBClient(**config)

    def save_cpu(self, cont_id, service, cpu_percentage):
        data = [{
            'measurement': 'cpu_usage',
            'tags': {
                'container_id': cont_id,
                'service': service
            },
            'fields': {
                'percentage': cpu_percentage
            }
        }]

        return self.db_connection.write_points(data)

    def save_memory(self, cont_id, service, memory_percentage):
        data = [{
            'measurement': 'memory_usage',
            'tags': {
                'container_id': cont_id,
                'service': service
            },
            'fields': {
                'percentage': memory_percentage
            }
        }]

        return self.db_connection.write_points(data)

    def save_blockio_bytes(self, cont_id, service, block_read, block_write):
        data = [{
            'measurement': 'blockio',
            'tags': {
                'container_id': cont_id,
                'service': service
            },
            'fields': {
                'read_bytes': block_read,
                'write_bytes': block_write
            }
        }]

        return self.db_connection.write_points(data)

    def __del__(self):
        self.db_connection.close()
