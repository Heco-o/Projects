import itertools
total = {}
ttt = ["xeeeeeeee", "xoeeeeeee", "xoxeeeeee", "xoxoeeeee", "xoxoxeeee", "xoxoxoeee", "xoxoxoxee", "xoxoxoxoe", "xoxoxoxox"]
for i in range(len(ttt)):
	z = sorted(list(set(itertools.permutations(ttt[i]))))
	total[i] = z
overall = []
for i in total.values():
	overall += i
for i in range(len(overall)):
	overall[i] = ((overall[i][0], overall[i][1], overall[i][2]),
						 (overall[i][3], overall[i][4], overall[i][5]),
						 (overall[i][6], overall[i][7], overall[i][8]))

overstr = f"{overall[0][0][0]} {overall[0][0][1]} {overall[0][0][2]}\n{overall[0][1][0]} {overall[0][1][1]} {overall[0][1][2]}\n{overall[0][2][0]} {overall[0][2][1]} {overall[0][2][2]}"
overall.pop(0)
for i in overall:
	overstr += "\n\n" + f"{i[0][0]} {i[0][1]} {i[0][2]}\n{i[1][0]} {i[1][1]} {i[1][2]}\n{i[2][0]} {i[2][1]} {i[2][2]}"
print(overstr)
with open("positions", "w") as file:
	file.write(overstr)