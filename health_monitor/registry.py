import mysql.connector as mysql


class MySQLRegistry:
    def __init__(self, config):
        self.db_connection = mysql.connect(**config)
        self.db_cursor = self.db_connection.cursor(prepared=True)

    def execute_parameterized_write(self, query, values):
        self.db_cursor.execute(query, values)
        self.db_connection.commit()
        print('write executed')

    def execute_parameterized_query(self, query, values):
        self.db_cursor.execute(query, values)
        print('read executed')

        return self.db_cursor.fetchall()

    def get_service_instances(self, service):
        query = 'SELECT ip_addr, port FROM Containers WHERE service = %s'

        return self.execute_parameterized_query(query, (service,))

    def entry_exists(self, cont_id, ip):
        query = 'SELECT * FROM Containers WHERE containerID = %s AND IP = %s'
        result = self.execute_parameterized_query(query, (cont_id, ip,))

        return len(result) != 0

    def add(self, cont_id, node_id, service, ip_addr, port, status):
        if not self.entry_exists(cont_id, ip_addr):
            query = 'INSERT INTO Containers VALUES(%s, %s, %s, %s, %s, %s)'
            values = (cont_id, node_id, service, ip_addr, port, status)

            self.execute_parameterized_write(query, values)

    def remove(self, cont_id, cont_ip=None):
        if cont_ip:
            if self.entry_exists(cont_id, cont_ip):
                query = 'DELETE FROM Containers WHERE containerID = %s and IP = %s'
                self.execute_parameterized_write(query, (cont_id, cont_ip,))
        else:
            query = 'DELETE FROM Containers WHERE containerID = %s'
            self.execute_parameterized_write(query, (cont_id,))

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()
