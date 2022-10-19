import socket
import pickle

class Talker:
	def __init__(self, host):
		self.host = host
		self.recv_board = False
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect()

	def display_message(self, message):
		print(f"Server: {message}")

	def react(self, data):
		if data[0] == "board":
			return data[1]

		if data[0] == "display_message":
			self.display_message(data[1])
			return False

		return False

	def recv(self, size=1024):
		data = pickle.loads(self.conn.recv(size))

		output = self.react(data)

		return output

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

	def next(self):
		self.recv_board = True
		while True:
			output = self.recv(1024)
			if not output == False:
				return output
		

	def send(self, board):
		bits = pickle.dumps(board)
		self.conn.sendall(bits)

	def send_next(self, board=False):
		try:
			if self.recv_board and not False:
				self.send(board)
			return self.next()
		except:
			self.connect()