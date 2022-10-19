import socket
from pickle import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.0.71"
port = 4545

server.bind((host, port))

server.listen()

while True:
	try:
		print("Waitting for player 1")

		player1, addr1 = server.accept()

		print("Sending ficha to player1")

		player1.sendall(b"x")

		print("Waitting for player 2")

		player2, addr2 = server.accept()

		print("Sending ficha to player2")

		player2.sendall(b"o")

		board = [[" " for b in range(7)] for a in range(6)]

		print("Board created")

		while True:
			print("Sending board to player 1")

			player1.sendall(dumps(board))

			board = loads(player1.recv(2024))

			print("Sending board to player 2")

			player2.sendall(dumps(board))

			board = loads(player2.recv(2024))	
	except:
		pass