# from dockerenv.client import DockerSDKClient
# from service_registration.registrar import Registrar

# docker_client = DockerSDKClient()
# registrar = Registrar(docker_client)

# registrar.start()

# from datetime import datetime, timedelta
# import configparser
# from influxdb import InfluxDBClient

# client = InfluxDBClient(host='localhost', port=8086,
#                         username='chocho', password='CH33a55b88d', database='metrics')

# client.drop_measurement('cpu_usage')

# query = 'select * from cpu_usage where service = $service'
# bind_params = {
#     'service': 'test'
# }

# data = [
#     {
#         'measurement': 'cpu_usage',
#         'tags': {
#             'container_id': '1',
#             'service': 'test'
#         },
#         'fields': {
#             'percentage': 10.0
#         }
#     },
#     {
#         'measurement': 'cpu_usage',
#         'tags': {
#             'container_id': '2',
#             'service': 'test2'
#         },
#         'fields': {
#             'percentage': 20.0
#         }
#     }
# ]

# print('==> write result <==')
# print(client.write_points(data))

# print('\n==> measurements <==')
# print(client.get_list_measurements())

# print('\n==> query <==')
# print(client.query(query=query, bind_params=bind_params))

# days = 1
# time = datetime.now() - timedelta(days=days)
# timestamp = time.isoformat('T') + 'Z'

# # timestamp2 = time.strftime('%Y-%m-%dT%H:%M:%SZ')
# print('timestamp: ', timestamp)

# query = (
#     "select mean(percentage) "
#     "from cpu_usage "
#     "where container_id = $id and time >= $period"
# )
# bind_params = {
#     'id': '1',
#     'period': timestamp
# }

# mean_cpu = client.query(
#     query=query, bind_params=bind_params)

# generator = mean_cpu.get_points(measurement='cpu_usage')

# print('\n==> mean cpu <==')
# print(next(generator))

# data = [{
#     'measurement': 'blockio',
#     'tags': {
#         'container_id': 'testc',
#         'service': 'test'
#     },
#     'fields': {
#         'read_bytes': 1000,
#         'write_bytes': 10
#     }
# }]

# client.write_points(data)

# query = (
#     "select read_bytes, write_bytes "
#     "from blockio "
#     "where container_id = $id"
# )
# bind_params = {
#     'id': 'testc'
# }

# blockio = client.query(
#     query=query, bind_params=bind_params)

# generator = blockio.get_points(measurement='blockio')

# print('\n==> blockio <==')
# print(next(generator))

# cont_query = (
#     "select mean(percentage) into cpu_mean "
#     "from cpu_usage "
#     "group by time(1m)"
# )

# client.create_continuous_query(
#     name='cpu_mean', select=cont_query, resample_opts='EVERY 10s for 2m')

# client.close()

# print('\n==> influx config <==')
# conf = configparser.ConfigParser()
# conf.read('test.ini')

# config = dict(conf.items('influxDB'))
# print(config)


import docker
import json

client = docker.from_env()

container = client.containers.list()[0]
container_raw = container.attrs
env = container_raw["Config"]["Env"]


print(env[4])