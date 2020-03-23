import requests
import socket
from errors import HttpCheckFailedException, TCPCheckFailedException, HttpConnectionException, TCPConnectionExcpetion, HttpTimeoutException, TCPTimeoutException

def http_check(ip, port, endpoint, status_code=200, timeout=0, headers={}):
	url = "http://" + ip + ":" + port + endpoint

	try:
		r = requests.get(url, timeout=timeout, headers=headers)

	except requests.exceptions.ConnectionError:
		raise HttpConnectionException(url)

	except requests.exceptions.Timeout:
		raise HttpTimeoutException(url)

	if r.status_code != status_code:
		raise HttpCheckFailedException(url, r.status_code)
	
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