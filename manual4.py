from talker import Talker

try:
	talker = Talker("192.168.0.86")

	board = talker.send_next()

	if len(board) > 0:
		talker.change_mode([(len(board[0])+4)*2, int((len(board))*1.7)])
	while talker.game_running:
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




