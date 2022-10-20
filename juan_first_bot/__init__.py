class Bot:
	def __init__(self):
		self.enemy_moves = []
		self.own_moves = []

	def display_group(self, group, size=20):
		board = [[" " for e in range(size)] for a in range(size)]
		for ficha in group[1]:
			board[ficha[1][1]][ficha[1][0]] = ficha[0]
		print("-"*size)
		for filas in board:
			for ficha in filas:
				print(f"{ficha}", end="", flush=False)
			print("|")
		print("-"*size)

	def distance_(self, pos1, pos2):
		return [abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])]

	def check_winner(self, board, n_fichas=4, fichas=["x", "o"]):
		for ficha in fichas:
			if self.check_done(ficha, board, n_fichas):
				return ficha
		return False

	def check_done(self, ficha, board, n_fichas=4):
		for g in self.get_groups(ficha, board):
			if len(g[1]) == n_fichas:
				return True
		return False

	def get_groups(self, ficha, board):
		groups = []
		fichas = self.get_fichas(ficha, board)
		for i in range(2):
			for ficha in fichas:
				for g in groups:
					if len(g[1]) == 1:
						distance = self.distance_(ficha[1], g[2])
						if distance == [0, 1]:
							#print("horizontal")
							g[1].append(ficha)
							g[0] = distance
						if distance == [1, 0]:
							#print("vertical")
							g[1].append(ficha)
							g[0] = distance
					else:
						if not ficha in g[1]:
							for mini_ficha in g[1]:
								if g[0] == self.distance_(ficha[1], mini_ficha[1]):
									g[1].append(ficha)							
				
				groups.append([[], [ficha], ficha[1]])
		bad_groups = []
		for g in groups:
			for g2 in groups:
				if not g[2] == g2[2] and g[2] == g2[2]:
					similar = False
					for mini_ficha in g[1]:
						for mini_ficha2 in g2[1]:
							if self.distance_(mini_ficha[1], mini_ficha2[1]) == g[0]:
								g[1] += g2[1]
								similar = True
								bad_groups.append(groups.index(g2))
								break
						if similar:
							break
		for bad in bad_groups[::-1]:
			pass
			#ºdel groups[bad]

					

		filtered_groups = []
		for g in groups:
			if len(g[1]) > 1:
				filtered_groups.append(g)
		return filtered_groups

	def get_fichas(self, ficha, board):
		#print(board)
		fichas = []
		y = 0
		for filas in board:
			x = 0
			if ficha in filas:
				for casilla in filas:
					if casilla == ficha:
						fichas.append([casilla, [x, y]])

					x+=1
			#print(filas, 0)
			y+=1
		#print(fichas)
		return fichas

	def calculate_moves(self, ficha, board):
		groups = self.get_groups(ficha, board)
		for g in groups:
			self.display_group(g)