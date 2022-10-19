from talker import Talker

talker = Talker("192.168.0.71")

board = talker.send_next()

def pr_board(board):
    for i in range(len(board)):
        print("|"+"|".join(board[i])+"|")

while True:
	pr_board(board)

	x = int(input("x:"))

	for i in range(len(board)):
		mmax = (len(board)-1)
		if board[mmax-i][x] == " ":
			board[mmax-i][x] = talker.ficha
			break

	pr_board(board)

	board = talker.send_next(board)
