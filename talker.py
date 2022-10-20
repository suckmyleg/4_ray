import socket
import pickle
import os

class Talker:
	def __init__(self, host, clear=True):
		self.host = host
		self.recv_board = False
		self.cls = clear
		self.connect()

	def pr_board(self, board):
		if self.cls:
			os.system("cls")
		for i in range(len(board)):
			print("|"+"|".join(board[i])+"|")

	def display_message(self, message):
		print(f"Server: {message}")

	def disconnected(self, message):
		if message:
			self.display_message(message)
		self.display_message("Disconnected")
		self.conn.close()

	def react(self, data):
		if data[0] == "board":
			return data[1]

		if data[0] == "pr_board":
			self.pr_board(data[1])
			return False

		if data[0] == "display_message":
			self.display_message(data[1])
			return False

		return False

	def recv(self, size=1024):
		try:
			data = pickle.loads(self.conn.recv(size))

			output = self.react(data)

			return output
		except:
			input("Disconnected")
			return True

	def connect(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Connecting", end="", flush=False)
		while True:
			try:
				self.conn.connect((self.host, 4545))
			except:
				print("\rRetrying...", end="   ", flush=False)
			else:
				print("\rConnected   ", end="\n", flush=False)
				break
		self.ficha = self.conn.recv(10).decode("utf-8")

	def next(self):
		self.recv_board = True
		while True:
			output = self.recv(250)
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