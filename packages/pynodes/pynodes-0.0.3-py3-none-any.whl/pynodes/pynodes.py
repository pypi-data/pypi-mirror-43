from pynodes.ext import santi
from flask import Flask, jsonify, request
from requests.exceptions import ConnectionError
import socket, _thread, requests, time, logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class Node(object):
	def __init__(self, addr, timeout=2):
		self.timeout = timeout
		self.addr = addr
		self.server = socket.socket()
		self.server.setsockopt(socket.SOL_SOCKET, 
			socket.SO_REUSEADDR, 1)
		self.server.bind(addr)
		self.server.listen(100)
		self.peers = {}
		self.stopthreads = False

	def checkpeerloop(self, check):
		while check():
			try:
				for peer in self.peers:
					conn = self.peers[peer]
					conn.settimeout(self.timeout)
					try:
						conn.send("nodealive".encode())
						r = conn.recv(1024)
					except (socket.timeout, ConnectionRefusedError, BrokenPipeError) as e:
						del self.peers[peer]
						conn.close()
			except RuntimeError:
				continue

	def getpeerloop(self, check):
		while check():
			net = santi.map_network()
			for ip in net:
				if ("%s:%i" % (ip, self.addr[1])) in self.peers:
					continue
				s = socket.socket()
				s.settimeout(self.timeout)
				try:
					s.connect((ip, self.addr[1]))
					self.peers["%s:%i" % (ip, self.addr[1])] = s
				except (socket.timeout, ConnectionRefusedError) as e:
					pass

	def acceptpeerloop(self, check):
		while check():
			conn, addr = self.server.accept()
			if ("%s:%i" % addr) in self.peers:
				continue
			self.peers["%s:%i" % addr] = conn

	def start(self, check=None):
		check = (lambda: not self.stopthreads) if check is None else check
		_thread.start_new_thread(self.getpeerloop, (check,))
		_thread.start_new_thread(self.checkpeerloop, (check,))
		_thread.start_new_thread(self.acceptpeerloop, (check,))
	def stop(self):
		self.stopthreads = True

class NodeHub(object):
	def __init__(self, node, url):
		self.node = node
		self.url = url
		self.hubs = []
		self.stopthreads = False
	def checkhubthread(self, check):
		while check():
			for url in self.hubs:
				try:
					r = requests.get(url+"/check")
					if not r.content == "alive":
						self.hubs.remove(url)
				except ConnectionError:
					self.hubs.remove(url)
	def checkpeerthread(self, check):
		while check():
			for url in self.hubs:
				try:
					peerlist = requests.get(url+"/hubs").json()
					if not self.hubs == peerlist:
						for new in peerlist:
							if not new in self.hubs:
								self.hubs.append(new)
								r = requests.get(new+"/register?url="+self.url)

					nodelist = request.get(url+"/node/peers").json()
					for addr in nodelist:
						if addr in self.node.peers:
							continue
						try:
							conn = socket.socket()
							conn.settimeout(1)
							conn.connect((addr.split(":")[0], int(addr.split(":")[1])))
							self.node.peers[addr] = conn
						except (socket.timeout, ConnectionRefusedError) as e:
							pass
				except ConnectionError:
					self.hubs.remove(url)
				except:
					pass # bad practice, i know

	def _start_api(self, addr):
		app = Flask(__name__)
		@app.route("/check")
		def app_check():
			return "alive"
		@app.route("/hubs")
		def app_peers():
			return jsonify(self.hubs)
		@app.route("/register")
		def app_register():
			hub = request.args['url'] # need a better way
			self.hubs.append(hub)
			r = requests.get(hub+"/register?url="+self.url)
		@app.route("/node/peers")
		def app_node_peers():
			return jsonify([i for i in self.node.peers])
		app.run(host=addr[0], port=addr[1])

	def start(self, addr, check=None):
		check = (lambda: not self.stopthreads) if check is None else check
		_thread.start_new_thread(self._start_api, (addr,))
		_thread.start_new_thread(self.checkhubthread, (check,))
		_thread.start_new_thread(self.checkpeerthread, (check,))