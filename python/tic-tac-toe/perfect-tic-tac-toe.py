import itertools
import json
from collections import defaultdict
total = {}
ttt = ["xeeeeeeee", "xoeeeeeee", "xoxeeeeee", "xoxoeeeee", "xoxoxeeee", "xoxoxoeee", "xoxoxoxee", "xoxoxoxoe", "xoxoxoxox"]
for i in range(len(ttt)):
	total[i + 1] = sorted(["".join(j) for j in set(itertools.permutations(ttt[i]))])

states = {"impossible":0, "Xwin":0, "Owin":0, "draw":0, "incomplete":0}
overall = {"impossible": defaultdict(list), "Xwin": defaultdict(list), "Owin": defaultdict(list), "draw": defaultdict(list), "incomplete": defaultdict(list)}

for key, value in total.items():
	for i in value:
		x = 0
		o = 0
		if (i[0] == "x" and i[1] == "x" and i[2] == "x"):
			x += 1
		elif (i[0] == "o" and i[1] == "o" and i[2] == "o"):
			o += 1
		if (i[3] == "x" and i[4] == "x" and i[5] == "x"):
			x += 1
		elif (i[3] == "o" and i[4] == "o" and i[5] == "o"):
			o += 1
		if (i[6] == "x" and i[7] == "x" and i[8] == "x"):
			x += 1
		elif (i[6] == "o" and i[7] == "o" and i[8] == "o"):
			o += 1
		if (i[0] == "x" and i[3] == "x" and i[6] == "x"):
			x += 1
		elif (i[0] == "o" and i[3] == "o" and i[6] == "o"):
			o += 1
		if (i[1] == "x" and i[4] == "x" and i[7] == "x"):
			x += 1
		elif (i[1] == "o" and i[4] == "o" and i[7] == "o"):
			o += 1
		if (i[2] == "x" and i[5] == "x" and i[8] == "x"):
			x += 1
		elif (i[2] == "o" and i[5] == "o" and i[8] == "o"):
			o += 1
		if (i[0] == "x" and i[4] == "x" and i[8] == "x"):
			x += 1
		elif (i[0] == "o" and i[4] == "o" and i[8] == "o"):
			o += 1
		if (i[2] == "x" and i[4] == "x" and i[6] == "x"):
			x += 1
		elif (i[2] == "o" and i[4] == "o" and i[6] == "o"):
			o += 1
		if x == 2:
			states["Xwin"] += 1
			overall["Xwin"][key].append(i)
		elif x == 0 and o == 0 and i.count("e") == 0:
			states["draw"] += 1
			overall["draw"][key].append(i)
		elif x == 1 and o == 0:
			if (9 - i.count("e")) % 2 == 1:
				states["Xwin"] += 1
				overall["Xwin"][key].append(i)
			else:
				states["impossible"] += 1
				overall["impossible"][key].append(i)
		elif x == 0 and o == 1:
			if (9 - i.count("e")) % 2 == 0:
				states["Owin"] += 1
				overall["Owin"][key].append(i)
			else:
				states["impossible"] += 1
				overall["impossible"][key].append(i)
		elif x + o > 1:
			states["impossible"] += 1
			overall["impossible"][key].append(i)
		else:
			states["incomplete"] += 1
			overall["incomplete"][key].append(i)

for key, value in overall.items():
	for i, j in value.items():
		value[i] = sorted(j)
	overall[key] = dict(value)

print(overall)
print(states)
"""
js = json.dumps(overall)
with open("positions.json", "w") as file:
	file.write(js)
"""