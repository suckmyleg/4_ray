from talker import Talker

talker = Talker("192.168.0.71")

board = talker.send_next()

while True:
	print("\n\n\n")
	for h in board:
		for x in h:
			print(x, end="", flush=False)

	x = int(input("x:"))

	for i in range(9):
		if board[8-i][x] == " ":
			board[8-i][x] = talker.ficha
			break

	board = talker.send_next(board)
