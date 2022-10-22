import socket
from pickle import *
import juan_first_bot as juan_bot
import time
from threading import Thread as th

class Player:
	def __init__(self, conn, addr, ficha):
		self.conn = conn
		self.addr = addr
		self.ficha = ficha

		print("Sending ficha to player1")

		time.sleep(0.01)
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
		self.send_command("win", "You've won")

	def loose(self):
		self.send_command("lost", "You've lost")
		
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

	def pr_board(self, board):
		if len(board[0]) == 0:
			return None
		for i in range(len(board)):
			print("|"+"|".join(board[i])+"|" + str(i))
		print("|"+" ".join([str(a) for a in range(len(board[0]))])+"|")

	def setup_connection(self):
		try:
			self.conn.bind((self.host, self.port))
			self.conn.listen()
		except Exception as e:
			input("Error trying to setup connection :" + str(e))

	def ongoing_match(self, n_players, n_fichas, players):
		try:
			time.sleep(1)

			bot = juan_bot.Bot()

			board = [[" " for b in range(6)] for a in range(7)]

			print("Board created")

			game_unfinished = True

			turns = 7*6

			current_turn = 0

			while game_unfinished:
				for n in range(n_players):
					current_turn += 1
					#print("Sending board to player", n+1)

					player = players[n]

					for player_ in players:
						if not player == player_:
							player_.show_board(board)

					time.sleep(0.1)

					player.send(board)

					board = player.next()

					if not board == False:
						pass
						#self.pr_board(board)
					else:
						#print(f"Player with ficha {player.ficha} another value ({board})")
						pass

					#print("Checking board")

					winner = bot.check_winner(board, n_fichas=n_fichas, fichas=self.fichas)

					emp = current_turn == turns

					if winner or emp:
						print("Player", winner, "won.")
						for player_ in players:
							player_.show_board(board)
							if player_.ficha == winner or emp:
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


	def start_match(self, n_players=3, n_fichas=4):
		while True:
			players = []
			try:
				for n in range(n_players):
					print("Waitting for player", n+1)
					conn, addr = self.conn.accept()
					player = Player(conn, addr, self.fichas[n])
					players.append(player)
			except Exception as e:
				print(e)
				for player in players:
					try:
						player.disconnected(str(e))
					except:
						pass
			else:
				th(target=self.ongoing_match, args=(n_players, n_fichas, players)).start()
s = Server("192.168.56.1", 4545)

s.start_match(2)