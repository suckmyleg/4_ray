import socket
import pickle

class Talker:
	def __init__(self, host):
		self.host = host
		self.recv_board = False
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect()

	def connect(self):
		print("Connecting", end="", flush=False)
		while True:
			try:
				self.conn.connect((self.host, 4545))
			except:
				print("\rRetrying...", end="   ", flush=False)
			else:
				print("\rConnected")
				break
		self.ficha = self.conn.recv(10).decode("utf-8")
		print("Ficha selected", self.ficha)

	def next(self):
		self.recv_board = True
		return pickle.loads(self.conn.recv(2024))

	def send(self, board):
		bits = pickle.dumps(board)
		print("Sending", len(bits), "bytes")
		self.conn.sendall(bits)

	def send_next(self, board=False):
		if self.recv_board and not False:
			self.send(board)
		return self.next()