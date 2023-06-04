import random
from collections import defaultdict

z = {}
b = [0,1,2,3,4,5,6,7,8]
while len(z) != 6045:
	a = ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty" , "Empty"]
	random.shuffle(b)
	for i in range(9):
		a[b[i]] = "X" if i % 2 == 0 else "O"
		z[tuple(a)] = 9 - a.count("Empty")
	print(len(z), end="\r")

reverse = defaultdict(list)
for key, value in z.items():
	reverse[value].append(list(key))
for key, value in reverse.items():
	reverse[key] = sorted(value)

y = sorted([i for key, value in reverse.items() for i in value])

z = {"imposible":0, "Xwin":0, "Owin":0, "draw":0, "uncomplete":0}
x = 0

for i in y:
	x = 0
	o = 0
	if (i[0] == "X" and i[1] == "X" and i[2] == "X"):
		x += 1
	elif (i[0] == "O" and i[1] == "O" and i[2] == "O"):
		o += 1
	if (i[3] == "X" and i[4] == "X" and i[5] == "X"):
		x += 1
	elif (i[3] == "O" and i[4] == "O" and i[5] == "O"):
		o += 1
	if (i[6] == "X" and i[7] == "X" and i[8] == "X"):
		x += 1
	elif (i[6] == "O" and i[7] == "O" and i[8] == "O"):
		o += 1
	if (i[0] == "X" and i[3] == "X" and i[6] == "X"):
		x += 1
	elif (i[0] == "O" and i[3] == "O" and i[6] == "O"):
		o += 1
	if (i[1] == "X" and i[4] == "X" and i[7] == "X"):
		x += 1
	elif (i[1] == "O" and i[4] == "O" and i[7] == "O"):
		o += 1
	if (i[2] == "X" and i[5] == "X" and i[8] == "X"):
		x += 1
	elif (i[2] == "O" and i[5] == "O" and i[8] == "O"):
		o += 1
	if (i[0] == "X" and i[4] == "X" and i[8] == "X"):
		x += 1
	elif (i[0] == "O" and i[4] == "O" and i[8] == "O"):
		o += 1
	if (i[2] == "X" and i[4] == "X" and i[6] == "X"):
		x += 1
	elif (i[2] == "O" and i[4] == "O" and i[6] == "O"):
		o += 1
	if x == 0 and o == 0 and i.count("Empty") == 0:
		z["draw"] += 1
	elif x == 1 and o == 0:
		if (9 - i.count("Empty")) % 2 == 1:
			z["Xwin"] += 1
		else:
			z["imposible"] += 1
	elif x == 0 and o == 1:
		if (9 - i.count("Empty")) % 2 == 0:
			z["Owin"] += 1
		else:
			z["imposible"] += 1
	elif x + o > 1:
		z["imposible"] += 1
	else:
		z["uncomplete"] += 1
print(z)