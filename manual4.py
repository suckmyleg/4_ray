from talker import Talker

talker = Talker("192.168.0.71")

board = talker.send_next()

def pr_board(board):
    for i in range(len(board)):
        print("|"+"|".join(board[i])+"|")

while True:
	pr_board(board)


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

	pr_board(board)

	board = talker.send_next(board)