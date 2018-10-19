import json
import datetime
from collections import deque

class LruCache:
	def __init__(self, timeout=10, maxsize=10):
		self.timeout = timeout
		self.store = {}
		self.maxsize = maxsize
		self.queue = deque(maxlen=maxsize)

	def __refresh(self, key):
		try:
			self.queue.remove(key)
		except ValueError:
			pass
		self.queue.appendleft(key)
		self.store[key][0] = datetime.datetime.now().timestamp()

	def __getitem__(self, key):
		if not self.__contains__(key):
			raise KeyError
		self.__refresh(key)
		return self.store[key][1]

	def __setitem__(self, key, value, ts=None):
		if key not in self.store:
			if len(self.queue) == self.maxsize:
				lastkey = self.queue.pop()
				del self.store[lastkey]
		self.store.setdefault(key, [None, None])
		self.__refresh(key)
		if ts is None:
			ts = datetime.datetime.now().timestamp()
		self.store[key][0] = ts
		self.store[key][1] = value

	def __contains__(self, key):
		ts, val = self.store.get(key, (None, None))
		if ts is None:
			return False
		cur_ts = datetime.datetime.now().timestamp()
		if cur_ts > self.timeout + ts:
			self.queue.remove(key)
			del self.store[key]
			return False
		return True

	def get(self, k, d=None):
		try:
			return self[k]
		except KeyError:
			return d
