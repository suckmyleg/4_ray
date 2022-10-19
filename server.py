import socket
from pickle import *
#from bot import bot

class Player:
	def __init__(self, conn, addr, ficha):
		self.conn = conn
		self.addr = addr
		self.ficha = ficha

		print("Sending ficha to player1")

		self.conn.sendall(str(self.ficha).encode("utf-8"))

	def send_command(self, command, data):
		self.conn.sendall(dumps([command, data]))

	def win(self):
		self.send_command("display_message", "You've won")

	def loose(self):
		self.send_command("display_message", "You've lost")
		
	def next(self):
		return loads(self.conn.recv(2024))

	def send(self, board):
		self.send_command("board", board)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.0.71"
port = 4545

server.bind((host, port))

server.listen()

#b = Bot()

board = str("{}x\n".format(" "*9))*9

while True:
	try:
		print("Waitting for player 1")

		conn, addr = server.accept()

		player1 = Player(conn, addr, "x")

		print("Waitting for player 2")

		conn, addr = server.accept()

		player2 = Player(conn, addr, "o")

		board = [[" " for b in range(7)] for a in range(6)]

		print("Board created")

		while True:
			print("Sending board to player 1")

			player1.send(board)

			board = player1.next()

			print("Sending board to player 2")

			player2.send(board)

			board = player2.next()
	except Exception as e:
		print(e)