import requests
import socket
from errors import HttpCheckFailedException, TCPCheckFailedException, HttpConnectionException, TCPConnectionExcpetion, HttpTimeoutException, TCPTimeoutException
from utils import parse_period

def http_check(ip, port, endpoint, status_code=200, timeout='5s', headers={}):
	url = "http://" + ip + ":" + str(port) + endpoint
	timeout_seconds = parse_period(timeout)

	try:
		r = requests.get(url, timeout=timeout_seconds, headers=headers)
		print(r.status_code)

	except requests.exceptions.ConnectionError:
		raise HttpConnectionException(url)

	except requests.exceptions.Timeout:
		raise HttpTimeoutException(url)

	if r.status_code != status_code:
		raise HttpCheckFailedException(url, str(r.status_code))
	
def tcp_check(ip, port, timeout=0):
	s = socket.socket(socket.AF_INET)
	s.settimeout(timeout)

	try:
		s.connect((ip, port))
		message = "ping"
		s.send(message)
		reply = s.recv(64)

		if reply != message:
			raise TCPCheckFailedException(ip, reply)

	except socket.error:
		raise TCPConnectionExcpetion(ip)

	except socket.timeout:
		raise TCPTimeoutException(ip)

	finally:
		s.close()