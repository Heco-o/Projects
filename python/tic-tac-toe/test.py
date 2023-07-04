import json
import subprocess
with open("positions.json", "r") as file:
	positions = json.loads(file.read())

count = 0
fMain = {9: set(),8: set(),7: set(),6: set(),5: set(),4: set(),3: set(),2: set(),1: set()}
for i, j in positions["draw"].items():
	for x in j:
		fMain[int(i)].add(x)
for num in range(8):
	for main in fMain[9 - num]:
		for i in positions["incomplete"][str(8 - num)]:
			key0 = False
			for j in range(9):
				if i[j] == "e":
					continue
				if i[j] != main[j]:
					key0 = True
					break
			if key0:
				continue
			print(str(len(fMain[8 - num])) + "    ", end="\r")
			fMain[8 - num].add(i)
print(fMain)
print(count)
for i, j in fMain.items():
	print(i, len(j))
	count += len(j)
print(count)