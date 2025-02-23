import itertools
import threading
import json
#from ast import literal_eval

initCards = {"king": 2, "servant": 2, "slave": 2}
defaultCards = list(itertools.combinations(["king", "servant", "slave"], 2))
#defaultCards = tuple(itertools.combinations_with_replacement(["king", "servant", "slave"], 2))
defaultCards = tuple(itertools.product(defaultCards, defaultCards))

cards = (({"king": 2 + i[0].count("king"), "servant": 2 + i[0].count("servant"), "slave": 2 + i[0].count("slave")}, {"king": 2 + i[1].count("king"), "servant": 2 + i[1].count("servant"), "slave": 2 + i[1].count("slave")}, i[0] + i[1]) for i in defaultCards)
"""
def convert(data):
	temp = {}
	for k, v in data.items():
		if isinstance(k, tuple):
			if isinstance(v, dict):
				temp[str(k)] = convert(v)
			else:
				temp[str(k)] = v
		else:
			if isinstance(v, dict):
				temp[k] = convert(v)
			else:
				temp[k] = v
	return temp.copy()
"""
#convert = lambda data: {str(k) if isinstance(k, tuple) else k: convert(v) if isinstance(v, dict) else v for k, v in data.items()}

#bConvert = lambda data: {literal_eval(k) if isinstance(k, str) else k: bConvert(v) if isinstance(v, dict) else v for k, v in data.items()}
#hook = lambda obj: tuple(obj) if isinstance(obj, list) else {k: hook(v) for k, v in obj.items()} if isinstance(obj, dict) else obj
#bConvert = lambda data: {literal_eval(k) if isinstance(k, str) else k: bConvert(v) for k, v in data.items()} if isinstance(data, dict) else tuple(data) if isinstance(data, list) else data


def check(Tuple, cards1, cards2, point1 = 0, point2 = 0):
	if Tuple[0] == "king":
		if Tuple[1] == "king":
			cards1["king"] -= 1
			cards2["king"] -= 1
		elif Tuple[1] == "servant":
			point1 += 1
			cards1["king"] -= 1
			cards2["servant"] -= 1
		elif Tuple[1] == "slave":
			point2 += 1
			cards1["king"] -= 1
			cards2["slave"] -= 1
	elif Tuple[0] == "servant":
		if Tuple[1] == "king":
			point2 += 1
			cards1["servant"] -= 1
			cards2["king"] -= 1
		elif Tuple[1] == "servant":
			cards1["servant"] -= 1
			cards2["servant"] -= 1
		elif Tuple[1] == "slave":
			point1 += 1
			cards1["servant"] -= 1
			cards2["slave"] -= 1
	elif Tuple[0] == "slave":
		if Tuple[1] == "king":
			point1 += 1
			cards1["slave"] -= 1
			cards2["king"] -= 1
		elif Tuple[1] == "servant":
			point2 += 1
			cards1["slave"] -= 1
			cards2["servant"] -= 1
		elif Tuple[1] == "slave":
			cards1["slave"] -= 1
			cards2["slave"] -= 1
	
	if "king" in cards1 and cards1["king"] <= 0:
		cards1.pop("king")
	elif "servant" in cards1 and cards1["servant"] <= 0:
		cards1.pop("servant")
	elif "slave" in cards1 and cards1["slave"] <= 0:
		cards1.pop("slave")
	
	if "king" in cards2 and cards2["king"] <= 0:
		cards2.pop("king")
	elif "servant" in cards2 and cards2["servant"] <= 0:
		cards2.pop("servant")
	elif "slave" in cards2 and cards2["slave"] <= 0:
		cards2.pop("slave")
	
	return point1, point2

games = []
positions = {}
running = True
count = 0
iterate = 0

def printLenPos():
	global games, count, running
	while running:
		#print(len(games), end='\r')
		print(count, end='\r')

TprintLenPos = threading.Thread(target=printLenPos)
TprintLenPos.start()
for card in cards:
	#iterate += 1
	positions1 = itertools.product(["king", "servant", "slave"], ["king", "servant", "slave"])
	position0 = card[2]
	positions[str(position0)] = (0, {})
	for position1 in positions1:
		#iterate += 1
		p1cards1 = card[0].copy()
		p2cards1 = card[1].copy()
		p1point1, p2point1 = check(position1, p1cards1, p2cards1)
		
		positions[str(position0)][1][str(position1)] = (0, {})
		positions2 = itertools.product(list(p1cards1.keys()), list(p2cards1.keys()))
		
		for position2 in positions2:
			#iterate += 1
			p1cards2 = p1cards1.copy()
			p2cards2 = p2cards1.copy()
			p1point2 = p1point1
			p2point2 = p2point1
			p1point2, p2point2 = check(position2, p1cards2, p2cards2, p1point2, p2point2)
			
			positions[str(position0)][1][str(position1)][1][str(position2)] = (0, {})
			positions3 = itertools.product(list(p1cards2.keys()), list(p2cards2.keys()))
			
			for position3 in positions3:
				#iterate += 1
				p1cards3 = p1cards2.copy()
				p2cards3 = p2cards2.copy()
				p1point3 = p1point2
				p2point3 = p2point2
				p1point3, p2point3 = check(position3, p1cards3, p2cards3, p1point3, p2point3)
				if p1point3 >= 3:
					#games.append((position1, position2, position3))
					count += 1
					positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)] = (100, None)
					continue
				elif p2point3 >= 3:
					#games.append((position1, position2, position3))
					count += 1
					positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)] = (-100, None)
					continue
				else:
					positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)] = (0, {})
				positions4 = itertools.product(list(p1cards3.keys()), list(p2cards3.keys()))
				
				for position4 in positions4:
					p1cards4 = p1cards3.copy()
					p2cards4 = p2cards3.copy()
					p1point4 = p1point3
					p2point4 = p2point3
					p1point4, p2point4 = check(position4, p1cards4, p2cards4, p1point4, p2point4)
					
					if p1point4 >= 3:
						#games.append((position1, position2, position3, position4))
						count += 1
						positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)] = (100, None)
						continue
					elif p2point4 >= 3:
						#games.append((position1, position2, position3, position4))
						count += 1
						positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)] = (-100, None)
						continue
					else:
						positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)] = (0, {})
					
					positions5 = itertools.product(list(p1cards4.keys()), list(p2cards4.keys()))
					
					for position5 in positions5:
						p1cards5 = p1cards4.copy()
						p2cards5 = p2cards4.copy()
						p1point5 = p1point4
						p2point5 = p2point4
						p1point5, p2point5 = check(position5, p1cards5, p2cards5, p1point5, p2point5)
						
						if p1point5 >= 3:
							#games.append((position1, position2, position3, position4, position5))
							count += 1
							positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)] = (100, None)
							continue
						elif p2point5 >= 3:
							#games.append((position1, position2, position3, position4, position5))
							count += 1
							positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)] = (-100, None)
							continue
						else:
							positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)] = (0, {})
						
						positions6 = itertools.product(list(p1cards5.keys()), list(p2cards5.keys()))
						
						for position6 in positions6:
							p1cards6 = p1cards5.copy()
							p2cards6 = p2cards5.copy()
							p1point6 = p1point5
							p2point6 = p2point5
							p1point6, p2point6 = check(position6, p1cards6, p2cards6, p1point6, p2point6)
							
							if p1point6 >= 3:
								#games.append((position1, position2, position3, position4, position5, position6))
								count += 1
								positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)] = (100, None)
								continue
							elif p2point6 >= 3:
								#games.append((position1, position2, position3, position4, position5, position6))
								count += 1
								positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)] = (-100, None)
								continue
							else:
								positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)] = (0, {})
							
							positions7 = itertools.product(list(p1cards6.keys()), list(p2cards6.keys()))
							
							for position7 in positions7:
								p1cards7 = p1cards6.copy()
								p2cards7 = p2cards6.copy()
								p1point7 = p1point6
								p2point7 = p2point6
								p1point7, p2point7 = check(position7, p1cards7, p2cards7, p1point7, p2point7)
								
								if p1point7 >= 3:
									#games.append((position1, position2, position3, position4, position5, position6, position7))
									count += 1
									positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)][1][str(position7)] = (100, None)
									continue
								elif p2point7 >= 3:
									#games.append((position1, position2, position3, position4, position5, position6, position7))
									count += 1
									positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)][1][str(position7)] = (-100, None)
									continue
								else:
									positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)][1][str(position7)] = (0, {})
								
								position8 = (list(p1cards7.keys())[0], list(p2cards7.keys())[0])
								p1cards8 = p1cards7.copy()
								p2cards8 = p2cards7.copy()
								p1point8 = p1point7
								p2point8 = p2point7
								p1point8, p2point8 = check(position8, p1cards8, p2cards8, p1point8, p2point8)
								
								if p1point8 >= 3 or p1point8 > p2point8:
									#games.append((position1, position2, position3, position4, position5, position6, position7, position8))
									count += 1
									positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)][1][str(position7)][1][str(position8)] = (100, None)
								elif p2point8 >= 3 or p2point8 > p1point8:
									#games.append((position1, position2, position3, position4, position5, position6, position7, position8))
									count += 1
									positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)][1][str(position7)][1][str(position8)] = (-100, None)
								else:
									#games.append((position1, position2, position3, position4, position5, position6, position7, position8))
									count += 1
									positions[str(position0)][1][str(position1)][1][str(position2)][1][str(position3)][1][str(position4)][1][str(position5)][1][str(position6)][1][str(position7)][1][str(position8)] = (0, None)
running = False
TprintLenPos.join()
print(count)
#print(iterate)



print("Deleting other variables...")
del itertools, threading
del check, printLenPos#, TprintLenPos
del initCards, defaultCards, cards, games
print("Done!")

#positions = convert(positions)
print("json.dump...")
positions = json.dumps(positions)
with open("positions.json", "w") as file:
	print("Writing positions.json...")
	file.write(positions)
	print("Done!")

#1336752