class HealthCheckException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)


class CheckAlreadyExistsException(HealthCheckException):
    def __init__(self, check_type):
        super().__init__("Check type " + check_type + " already exists")


class UnknownCheckTypeException(HealthCheckException):
    def __init__(self, check_type):
        super().__init__("Check type " + check_type + " does not exist")


class CheckConfigurationException(HealthCheckException):
    def __init__(self):
        super().__init__("Invalid health check configuration")


class HttpCheckFailedException(HealthCheckException):
    def __init__(self, url, status_code):
        super().__init__("Service at " + url +
                         " returned unexpected status code " + status_code)


class TCPCheckFailedException(HealthCheckException):
    def __init__(self, ip, reply):
        super().__init__("Bad reply from " + ip + ": " + reply)


class HttpTimeoutException(HealthCheckException):
    def __init__(self, url):
        super().__init__("Request to " + url + " timed out")


class TCPTimeoutException(HealthCheckException):
    def __init__(self, ip):
        super().__init__("Connection to " + ip + " timed out")


class HttpConnectionException(HealthCheckException):
    def __init__(self, url):
        super().__init__("Could not establish http connection with " + url)


class TCPConnectionExcpetion(HealthCheckException):
    def __init__(self, ip):
        super().__init__("Connection to " + ip + " failed")
