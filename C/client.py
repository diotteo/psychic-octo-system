#! /usr/bin/env python3

import socket
import select
import argparse

class CacheClient:
	def __init__(self, host, port=12345, bufsize=4096):
		self.host = host
		self.port = port
		self.bufsize = bufsize
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.host, self.port))

	def close(self):
		self.sock.close()

	def _send_request(self, data):
		self.sock.send(data.encode())

	def _recv_response(self):
		rd_s, wr_s, err_s = select.select([self.sock], [], [])
		data, addr = self.sock.recvfrom(self.bufsize)
		return data.decode()

	def read_key(self, key):
		self._send_request('\n'.join(('READ', key)))
		return self._recv_response()

	def write_key(self, key, data):
		self._send_request('\n'.join(('WRITE', key, data)))
		return self._recv_response()

	def dump_cache(self):
		self._send_request('DUMP')
		return self._recv_response()


def is_port(s):
	try:
		nb = int(s)
	except:
		raise argparse.ArgumentTypeError('port value is not an int')
	if nb < 1 or nb > 65535:
		raise argparse.ArgumentTypeError('port value out of range')
	return nb

def parse_args():
	parser = argparse.ArgumentParser(description='Launch cache server')
	parser.add_argument('--host', '-H', nargs='?', default='localhost')
	parser.add_argument('--port', '-p', nargs='?', type=is_port, default=12345)
	parser.add_argument('type')
	parser.add_argument('key', nargs='?')
	parser.add_argument('data', nargs='?')
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()

	client = None
	try:
		client = CacheClient(args.host, args.port)

		if args.type == 'read':
			resp = client.read_key(args.key)
			print(resp)
		elif args.type == 'write':
			resp = client.write_key(args.key, args.data)
			print(resp)
		elif args.type == 'dump':
			resp = client.dump_cache()
			print(resp)
		else:
			print('Not implemented')
	finally:
		if client:
			client.close()
