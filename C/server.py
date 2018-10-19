#! /usr/bin/env python3

import socket
import select
import traceback
import argparse

from cache import LruCache

class LruCacheServer:
	def __init__(self, host, port, recv_bufsize=4096, timeout=10, maxsize=10):
		self.host = host
		self.port = port
		self.cache = LruCache(timeout=timeout, maxsize=maxsize)
		self.bufsize = recv_bufsize

	def run(self):
		srv_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		srv_s.bind((self.host, self.port))
		srv_s.listen(5)

		conn_list = [srv_s]
		try:
			while True:
				rd_s, wr_s, err_s = select.select(conn_list, [], [])

				for sock in rd_s:
					if sock == srv_s:
						new_sock, addr = srv_s.accept()
						addr = new_sock.getpeername()
						conn_list.append(new_sock)
						print("Client ({}) connected".format(addr))
					else:
						try:
							data = sock.recv(self.bufsize)
							if data:
								self.parse_request(data.decode(), sock)
						except:
							traceback.print_last()
							sock.close()
							conn_list.remove(sock)
		finally:
			for sock in conn_list:
				sock.close()

	def parse_request(self, req_data, client_sock):
		lines = req_data.split(maxsplit=2)
		reqtype = lines[0]
		key = lines[1] if len(lines) > 1 else None

		if reqtype == 'READ':
			print('Reading {}'.format(key))
			if key not in self.cache:
				client_sock.send('Key {} not in cache'.format(key).encode())
			else:
				client_sock.send(self.cache[key].encode())
		elif reqtype == 'WRITE':
			print('Writing {}'.format(key))
			data = lines[2]
			self.cache[key] = data
			client_sock.send("Wrote {}".format(key).encode())
		elif reqtype == 'UPDATE':
			#TODO: Update needs to specify a timestamp
			print('Updating {} (not implemented)'.format(key))
			client_sock.send("Not implemented".encode())
		elif reqtype == 'DUMP':
			client_sock.send(str(self.cache.store.keys()).encode())
		else:
			print('Bogus request, ignoring...')
			client_sock.send('bogus'.encode())

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
	parser.add_argument('--maxsize', '-m', type=int, default=10)
	parser.add_argument('--timeout', '-t', type=int, default=10)
	parser.add_argument('--host', '-H', default='localhost')
	parser.add_argument('--port', '-p', type=is_port, default=12345)
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()

	server = LruCacheServer(args.host, args.port, timeout=args.timeout, maxsize=args.maxsize)
	server.run()
