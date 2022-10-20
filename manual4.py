from talker import Talker

try:

	talker = Talker("localhost")

	board = talker.send_next()

	def pr_board(board):
	    for i in range(len(board)):
	        print("|"+"|".join(board[i])+"|")

	while True:
		talker.pr_board(board)

		while True:
			x = int(input(f"{talker.ficha}:"))
			done = False
			try:
				for i in range(len(board)):
					mmax = (len(board)-1)
					if board[mmax-i][x] == " ":
						done = True
						board[mmax-i][x] = talker.ficha
						break

			except:
				pass
			else:
				if done:
					break

		board = talker.send_next(board)
except Exception as e:
	print(e)
	input()
