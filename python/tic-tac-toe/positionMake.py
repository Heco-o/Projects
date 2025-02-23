import threading
import json

positions = {}
positions1 = ('eeeeeeeex', 'eeeeeeexe', 'eeeeeexee', 'eeeeexeee', 'eeeexeeee', 'eeexeeeee', 'eexeeeeee', 'exeeeeeee', 'xeeeeeeee')

def check(Tuple):
	if (Tuple[0] == "x" and Tuple[1] == "x" and Tuple[2] == "x"):
		return 1
	elif (Tuple[0] == "o" and Tuple[1] == "o" and Tuple[2] == "o"):
		return -1
	if (Tuple[3] == "x" and Tuple[4] == "x" and Tuple[5] == "x"):
		return 1
	elif (Tuple[3] == "o" and Tuple[4] == "o" and Tuple[5] == "o"):
		return -1
	if (Tuple[6] == "x" and Tuple[7] == "x" and Tuple[8] == "x"):
		return 1
	elif (Tuple[6] == "o" and Tuple[7] == "o" and Tuple[8] == "o"):
		return -1
	if (Tuple[0] == "x" and Tuple[3] == "x" and Tuple[6] == "x"):
		return 1
	elif (Tuple[0] == "o" and Tuple[3] == "o" and Tuple[6] == "o"):
		return -1
	if (Tuple[1] == "x" and Tuple[4] == "x" and Tuple[7] == "x"):
		return 1
	elif (Tuple[1] == "o" and Tuple[4] == "o" and Tuple[7] == "o"):
		return -1
	if (Tuple[2] == "x" and Tuple[5] == "x" and Tuple[8] == "x"):
		return 1
	elif (Tuple[2] == "o" and Tuple[5] == "o" and Tuple[8] == "o"):
		return -1
	if (Tuple[0] == "x" and Tuple[4] == "x" and Tuple[8] == "x"):
		return 1
	elif (Tuple[0] == "o" and Tuple[4] == "o" and Tuple[8] == "o"):
		return -1
	if (Tuple[2] == "x" and Tuple[4] == "x" and Tuple[6] == "x"):
		return 1
	elif (Tuple[2] == "o" and Tuple[4] == "o" and Tuple[6] == "o"):
		return -1

def printLen():
	global counts, running
	while running:
		print(counts, end='\r')
draw = 0
xWin = 0
oWin = 0
counts = 0
running = True

TprintLen = threading.Thread(target=printLen)
TprintLen.start()

for position1 in positions1:
	positions[position1] = []
	positions[position1].append(0)
	positions[position1].append({})
	positions2 = tuple(sorted(position1[0:i] + "o" + position1[i+1:] for i in range(9) if position1[i] == "e"))
	for position2 in positions2:
		positions[position1][1][position2] = []
		positions[position1][1][position2].append(0)
		positions[position1][1][position2].append({})
		positions3 = tuple(sorted(position2[0:i] + "x" + position2[i+1:] for i in range(9) if position2[i] == "e"))
		for position3 in positions3:
			positions[position1][1][position2][1][position3] = []
			positions[position1][1][position2][1][position3].append(0)
			positions[position1][1][position2][1][position3].append({})
			positions4 = tuple(sorted(position3[0:i] + "o" + position3[i+1:] for i in range(9) if position3[i] == "e"))
			for position4 in positions4:
				positions[position1][1][position2][1][position3][1][position4] = []
				positions[position1][1][position2][1][position3][1][position4].append(0)
				positions[position1][1][position2][1][position3][1][position4].append({})
				positions5 = tuple(sorted(position4[0:i] + "x" + position4[i+1:] for i in range(9) if position4[i] == "e"))
				for position5 in positions5:
					positions[position1][1][position2][1][position3][1][position4][1][position5] = []
					positions[position1][1][position2][1][position3][1][position4][1][position5].append(0)
					positions[position1][1][position2][1][position3][1][position4][1][position5].append({})
					if (check(position5) == 1):
						positions[position1][1][position2][1][position3][1][position4][1][position5][0] = 1
						positions[position1][1][position2][1][position3][1][position4][1][position5][1] = None
						counts += 1
						xWin += 1
						continue
					positions6 = tuple(sorted(position5[0:i] + "o" + position5[i+1:] for i in range(9) if position5[i] == "e"))
					for position6 in positions6:
						positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6] = []
						positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6].append(0)
						positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6].append({})
						if (check(position6) == -1):
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][0] = -1
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1] = None
							counts += 1
							oWin += 1
							continue
						positions7 = tuple(sorted(position6[0:i] + "x" + position6[i+1:] for i in range(9) if position6[i] == "e"))
						for position7 in positions7:
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7] = []
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7].append(0)
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7].append({})
							if (check(position7) == 1):
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][0] = 1
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1] = None
								counts += 1
								xWin += 1
								continue
							positions8 = tuple(sorted(position7[0:i] + "o" + position7[i+1:] for i in range(9) if position7[i] == "e"))
							for position8 in positions8:
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8] = []
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8].append(0)
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8].append({})
								if (check(position8) == -1):
									positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][0] = -1
									positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][1] = None
									counts += 1
									oWin += 1
									continue
								position9 = position8.replace("e", "x")
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][1][position9] = []
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][1][position9].append(0)
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][1][position9].append(None)
								if (check(position9) == 1):
									positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][1][position9][0] = 1
									positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][1][position9][1] = None
									counts += 1
									xWin += 1
									continue
								counts += 1
								draw += 1

running = False
TprintLen.join()
print(counts)

for position1, list1 in positions.items():
	state1 = []
	for position2, list2 in list1[1].items():
		state2 = []
		for position3, list3 in list2[1].items():
			state3 = []
			for position4, list4 in list3[1].items():
				state4 = []
				for position5, list5 in list4[1].items():
					if list5[1] == None:
						state4.append(1)
						continue
					state5 = []
					for position6, list6 in list5[1].items():
						if list6[1] == None:
							state5.append(-1)
							continue
						state6 = []
						for position7, list7 in list6[1].items():
							if list7[1] == None:
								state6.append(1)
								continue
							state7 = []
							for position8, list8 in list7[1].items():
								if list8[1] == None:
									state7.append(-1)
									continue
								state8 = []
								for position9, list9 in list8[1].items():
									state8.append(list9[0])
								if 1 in state8:
									positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][0] = 1
									state7.append(1)
								elif 0 in state8:
									positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][0] = 0
									state7.append(0)
								elif -1 in state8:
									positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][1][position8][0] = -1
									state7.append(-1)
							if -1 in state7:
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][0] = -1
								state6.append(-1)
							elif 0 in state7:
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][0] = 0
								state6.append(0)
							elif 1 in state7:
								positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][1][position7][0] = 1
								state6.append(1)
						if 1 in state6:
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][0] = 1
							state5.append(1)
						elif 0 in state6:
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][0] = 0
							state5.append(0)
						elif -1 in state6:
							positions[position1][1][position2][1][position3][1][position4][1][position5][1][position6][0] = -1
							state5.append(-1)
					if -1 in state5:
						positions[position1][1][position2][1][position3][1][position4][1][position5][0] = -1
						state4.append(-1)
					elif 0 in state5:
						positions[position1][1][position2][1][position3][1][position4][1][position5][0] = 0
						state4.append(0)
					elif 1 in state5:
						positions[position1][1][position2][1][position3][1][position4][1][position5][0] = 1
						state4.append(1)
				if 1 in state4:
					positions[position1][1][position2][1][position3][1][position4][0] = 1
					state3.append(1)
				elif 0 in state4:
					positions[position1][1][position2][1][position3][1][position4][0] = 0
					state3.append(0)
				elif -1 in state4:
					positions[position1][1][position2][1][position3][1][position4][0] = -1
					state3.append(-1)
			if -1 in state3:
				positions[position1][1][position2][1][position3][0] = -1
				state2.append(-1)
			elif 0 in state3:
				positions[position1][1][position2][1][position3][0] = 0
				state2.append(0)
			elif 1 in state3:
				positions[position1][1][position2][1][position3][0] = 1
				state2.append(1)
		if 1 in state2:
			positions[position1][1][position2][0] = 1
			state1.append(1)
		elif 0 in state2:
			positions[position1][1][position2][0] = 0
			state1.append(0)
		elif -1 in state2:
			positions[position1][1][position2][0] = -1
			state1.append(-1)
	if -1 in state1:
		positions[position1][0] = -1
	elif 0 in state1:
		positions[position1][0] = 0
	elif 1 in state1:
		positions[position1][0] = 1
	print(positions[position1][0], end=", ", flush=True)

print(f"\nxWin: {xWin}, oWin: {oWin}, draw: {draw}")

js = json.dumps(positions)
with open("games.json", "w") as file:
	file.write(js)