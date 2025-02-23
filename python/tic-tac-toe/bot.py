import random
import json
with open("games.json", "r") as file:
	positions = json.loads(file.read())

def check(pos):
	if (pos[0] == "x" and pos[1] == "x" and pos[2] == "x"):
		return 1
	elif (pos[0] == "o" and pos[1] == "o" and pos[2] == "o"):
		return -1
	if (pos[3] == "x" and pos[4] == "x" and pos[5] == "x"):
		return 1
	elif (pos[3] == "o" and pos[4] == "o" and pos[5] == "o"):
		return -1
	if (pos[6] == "x" and pos[7] == "x" and pos[8] == "x"):
		return 1
	elif (pos[6] == "o" and pos[7] == "o" and pos[8] == "o"):
		return -1
	if (pos[0] == "x" and pos[3] == "x" and pos[6] == "x"):
		return 1
	elif (pos[0] == "o" and pos[3] == "o" and pos[6] == "o"):
		return -1
	if (pos[1] == "x" and pos[4] == "x" and pos[7] == "x"):
		return 1
	elif (pos[1] == "o" and pos[4] == "o" and pos[7] == "o"):
		return -1
	if (pos[2] == "x" and pos[5] == "x" and pos[8] == "x"):
		return 1
	elif (pos[2] == "o" and pos[5] == "o" and pos[8] == "o"):
		return -1
	if (pos[0] == "x" and pos[4] == "x" and pos[8] == "x"):
		return 1
	elif (pos[0] == "o" and pos[4] == "o" and pos[8] == "o"):
		return -1
	if (pos[2] == "x" and pos[4] == "x" and pos[6] == "x"):
		return 1
	elif (pos[2] == "o" and pos[4] == "o" and pos[6] == "o"):
		return -1
	return 0

def makeMove(pos, num):
	moves1 = [k for k, v in pos.items() if v[0] == num]
	moves2 = [k for k, v in pos.items() if v[0] == 0]
	moves3 = [k for k, v in pos.items() if v[0] == -num]
	
	if len(moves1) > 0:
		return random.choice(moves1)
	elif len(moves2) > 0:
		return random.choice(moves2)
	elif len(moves3) > 0:
		return random.choice(moves2)

def getMove(pos, turn):
	while move := list(input("Enter the move:\n").strip()):
		if len(move) == 2:
			if 3 >= int(move[0]) >= 1 and 3 >= int(move[1]) >= 1:
				move = 3*int(move[0]) + int(move[1]) - 4
				if pos[move] == "e":
					break
				else:
					print("You can't place in that position")
			else:
				print("xy coordinates is over the limit")
		else:
			print("Please enter the xy coordinates of your next move.")
	return pos[0:move] + turn + pos[move+1:]

def printMove(pos, last=None):
	pos = pos.replace("e", " ")
	print()
	print(pos[0], pos[1], pos[2])
	print(pos[3], pos[4], pos[5])
	if last == None:
		print(pos[6], pos[7], pos[8])
	else:
		num = ""
		for i in range(3):
			key = False
			for j in range(3):
				if pos[j+i*3] != last[j+i*3]:
					num = f"{i+1}{j+1}"
					key = True
					break
			if key:
				break
		print(pos[6], pos[7], pos[8], num)

while True:
	start = input("Enter:\n").lower()
	game = []
	if start.startswith("u"):
		move1 = makeMove(positions, 1)
		game.append(move1)
		printMove(move1, "eeeeeeeee")
		move2 = getMove(move1, "o")
		game.append(move2)
		printMove(move2)
		move3 = makeMove(positions[move1][1][move2][1], 1)
		game.append(move3)
		printMove(move3, move2)
		move4 = getMove(move3, "o")
		game.append(move4)
		printMove(move4)
		move5 = makeMove(positions[move1][1][move2][1][move3][1][move4][1], 1)
		game.append(move5)
		printMove(move5, move4)
		if check(move5) == 1:
			print("X Wins!")
			continue
		move6 = getMove(move5, "o")
		game.append(move6)
		printMove(move6)
		if check(move6) == -1:
			print("O Wins!")
			continue
		move7 = makeMove(positions[move1][1][move2][1][move3][1][move4][1][move5][1][move6][1], 1)
		game.append(move7)
		printMove(move7, move6)
		if check(move7) == 1:
			print("X Wins!")
			continue
		move8 = getMove(move7, "o")
		game.append(move8)
		printMove(move8)
		if check(move8) == -1:
			print("O Wins!")
			continue
		move9 = makeMove(positions[move1][1][move2][1][move3][1][move4][1][move5][1][move6][1][move7][1][move8][1], 1)
		game.append(move9)
		printMove(move9, move8)
		if check(move9) == 1:
			print("X Wins!")
			continue
		print("It's a Draw!")
	else:
		move1 = getMove("eeeeeeeee", "x")
		game.append(move1)
		printMove(move1)
		move2 = makeMove(positions[move1][1], -1)
		game.append(move2)
		printMove(move2, move1)
		move3 = getMove(move2, "x")
		game.append(move3)
		printMove(move3)
		move4 = makeMove(positions[move1][1][move2][1][move3][1], -1)
		game.append(move4)
		printMove(move4, move3)
		move5 = getMove(move4, "x")
		game.append(move5)
		printMove(move5)
		if check(move5) == 1:
			print("X Wins!")
			continue
		move6 = makeMove(positions[move1][1][move2][1][move3][1][move4][1][move5][1], -1)
		game.append(move6)
		printMove(move6, move5)
		if check(move6) == -1:
			print("O Wins!")
			continue
		move7 = getMove(move6, "x")
		game.append(move7)
		printMove(move7)
		if check(move7) == 1:
			print("X Wins!")
			continue
		move8 = makeMove(positions[move1][1][move2][1][move3][1][move4][1][move5][1][move6][1][move7][1], -1)
		game.append(move8)
		printMove(move8, move7)
		if check(move8) == -1:
			print("O Wins!")
			continue
		move9 = getMove(move8, "x")
		game.append(move9)
		printMove(move9)
		if check(move9) == 1:
			print("X Wins!")
			continue
		print("It's a Draw!")