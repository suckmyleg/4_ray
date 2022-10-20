import socket
import pickle
import os

class Talker:
	def __init__(self, host, clear=True):
		self.host = host
		self.recv_board = False
		self.game_running = False
		self.last_board = False
		self.win = None
		self.cls = clear
		self.connect()

	def pr_board(self, board):
		self.last_board = board
		if self.cls:
			os.system("cls")
		if len(board[0]) == 0:
			return None
		for i in range(len(board)):
			print("|"+"|".join(board[i])+"|" + str(i))
		print("|"+" ".join([str(a) for a in range(len(board[0]))])+"|")

	def change_mode(self, params):
		os.system(f"mode {params[0]}, {params[1]}")
		print(params)

	def display_message(self, message):
		print(f"Server: {message}")

	def win(self, message):
		if message:
			self.display_message(message)
		self.win = True

	def lost(self, message):
		if message:
			self.display_message(message)
		self.win = False

	def disconnected(self, message):
		if message:
			self.display_message(message)
		self.display_message("Disconnected")
		self.game_running = False
		self.conn.close()

	def react(self, data):
		if not self.game_running:
			return True

		if data[0] == "board":
			return data[1]

		if data[0] == "pr_board":
			self.pr_board(data[1])
			return False

		if data[0] == "win":
			self.win(data[1])
			return False

		if data[0] == "lost":
			self.lost(data[1])
			return False

		if data[0] == "display_message":
			self.display_message(data[1])
			return False

		return False

	def recv(self, size=1024):
		if not self.game_running:
			return True
		try:
			data = pickle.loads(self.conn.recv(size))

			output = self.react(data)

			return output
		except:
			self.game_running = False
			print("Disconnected")
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
		self.game_running = True

	def next(self):
		self.recv_board = True
		while self.game_running:
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