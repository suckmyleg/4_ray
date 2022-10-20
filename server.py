import socket
from pickle import *
import juan_bot

class Player:
	def __init__(self, conn, addr, ficha):
		self.conn = conn
		self.addr = addr
		self.ficha = ficha

		print("Sending ficha to player1")

		self.conn.sendall(str(self.ficha).encode("utf-8"))

	def send_command(self, command, data):
		self.conn.sendall(dumps([command, data]))

	def send_messages(self, messages=[]):
		for m in messages:
			self.send_command("display_message", m)

	def disconnected(self, message=False):
		self.send_command("disconnected", message)

	def show_board(self, board):
		self.send_command("pr_board", board)

	def win(self):
		self.send_command("display_message", "You've won")

	def loose(self):
		self.send_command("display_message", "You've lost")
		
	def next(self):
		return loads(self.conn.recv(2024))

	def send(self, board):
		self.send_command("board", board)

class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.fichas = ["x", "o", "l", "k", "z"]
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.setup_connection()

	def setup_connection(self):
		try:
			self.conn.bind((self.host, self.port))
			self.conn.listen()
		except Exception as e:
			input("Error trying to setup connection :" + str(e))

	def start_match(self, n_players=2, n_fichas=4):
		board = str("{}x\n".format(" "*9))*9

		while True:

			bot = juan_bot.Bot()

			players = []
			try:
				for n in range(n_players):
					print("Waitting for player", n+1)
					conn, addr = self.conn.accept()
					player = Player(conn, addr, self.fichas[n])
					players.append(player)

				board = [[" " for b in range(7)] for a in range(6)]

				print("Board created")

				game_unfinished = True

				while game_unfinished:
					for n in range(n_players):
						print("Sending board to player", n+1)

						player = players[n]

						for player_ in players:
							if not player == player_:
								player_.show_board(board)

						player.send(board)

						board = player.next()

						print("Checking board")

						winner = bot.check_winner(board, n_fichas=n_fichas, fichas=self.fichas)

						if winner:
							print("Player", winner, "won.")
							for player_ in players:
								player_.show_board(board)
								if player_.ficha == winner:
									player_.win()
								else:
									player_.loose()
							game_unfinished = False
							break
			except Exception as e:
				print(e)
				for player in players:
					try:
						player.disconnected(str(e))
					except:
						pass


s = Server("localhost", 4545)

s.start_match(2)