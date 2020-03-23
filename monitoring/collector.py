from datetime import datetime
import concurrent.futures


class Collector:
    def __init__(self, docker_client, scheduler, metrics_store, interval):
        self.docker_client = docker_client
        self.scheduler = scheduler
        self.metrics_store = metrics_store
        self.interval = interval

    def start(self):
        # schedule run here
        self.scheduler.add_job(
            self.run, 'interval', seconds=self.interval, next_run_time=datetime.now())
        self.scheduler.start()

    def run(self):
        # collect metrics for each container
        print('running\n')
        containers = self.docker_client.get_containers()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.collect, containers)

    def collect(self, container):
        # obtains metrics for the container
        # writes metrics in the database
        cont_id = container.id
        service = container.labels['com.docker.swarm.service.name']

        container_stats = self.docker_client.get_container_stats(cont_id)
        cpu_stats = container_stats['cpu_stats']
        precpu_stats = container_stats['precpu_stats']
        memory_stats = container_stats['memory_stats']
        blkio_stats = container_stats['blkio_stats']

        cpu_usage = self.calc_cpu_usage(cpu_stats, precpu_stats)
        mem_usage = self.calc_memory_usage(memory_stats)
        block_read, block_write = self.calc_block_io(blkio_stats)

        print(container.name)
        print('cpu usage: ', cpu_usage, '%')
        print('memory usage: ', mem_usage, '%')
        print('block io read/write: ', block_read, '/', block_write, '\n')

        self.metrics_store.save_cpu(cont_id, service, cpu_usage)
        self.metrics_store.save_memory(cont_id, service, mem_usage)
        self.metrics_store.save_blockio_bytes(
            cont_id, service, block_read, block_write)

        # perform error handling

    def calc_cpu_usage(self, cpu_stats, precpu_stats):
        # extract current percantage of CPU usage for container
        cpu_percent = 0.0

        current_cpu = cpu_stats['cpu_usage']['total_usage']
        previous_cpu = precpu_stats['cpu_usage']['total_usage']

        current_system = cpu_stats['system_cpu_usage']
        previous_system = precpu_stats['system_cpu_usage']

        cpu_delta = current_cpu - previous_cpu
        system_delta = current_system - previous_system
        online_cpus = cpu_stats['online_cpus']

        if (online_cpus == 0.0):
            online_cpus = len(cpu_stats['cpu_usage']['percpu_usage'])

        if system_delta > 0.0 and cpu_delta > 0.0:
            cpu_percent = (cpu_delta / system_delta) * online_cpus * 100.0

        return cpu_percent

    def calc_memory_usage(self, memory_stats):
        # extract current percentage of memory usage for container
        memory_percent = 0.0

        memory_usage = memory_stats['usage'] - memory_stats['stats']['cache']
        limit = memory_stats['limit']

        if limit != 0:
            memory_percent = (memory_usage / limit) * 100.0

        return memory_percent

    def calc_block_io(self, blkio_stats):
        # extract number of bytes in read and write io operations
        block_read = 0
        block_write = 0

        for bio_entry in blkio_stats['io_service_bytes_recursive']:
            if bio_entry['op'] == 'Read':
                block_read = block_read + bio_entry['value']
            elif bio_entry['op'] == 'Write':
                block_write = block_write + bio_entry['value']

        return block_read, block_write
