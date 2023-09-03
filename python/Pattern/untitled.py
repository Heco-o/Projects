import argparse
import threading
import time

stime = time.time()
run = threading.Event()
run.set()
animation = ["Please wait    ", "Please wait.   ", "Please wait..  ", "Please wait... ", "Please wait...."]
def animate():
	index = 0
	while run.is_set():
		print(animation[index % len(animation)], end="\r")
		index += 1
		time.sleep(0.2)

animate = threading.Thread(target=animate)
animate.start()

parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store_true")
S = parser.parse_args().s

try:
	import sympy
except ModuleNotFoundError as E:
	run.clear()
	animate.join()
	print(E)
	print("sympy module is required\nrun 'pip3 install sympy' to download the module")
	exit()

def difference(x):
	alist = [x[i + 1] - x[i] for i in range(len(x) - 1)]
	return alist.copy(), all(True if alist[i] == alist[i + 1] else False for i in range(len(alist) - 1)), alist[0]

def create(n, x, d):
	facto = 1
	temp = "(n - 1)"
	for i in range(2, n + 2):
		temp += f"*(n - {i})"
		facto *= i
	return f"({x}) + (({d})*({temp}))/{facto}"

run.clear()
animate.join()

print("\nDone!")
print("Finished in " + str(time.time() - stime) + " seconds\n")

inputs = "".join(input("Enter a pattern:\n").split()).split(",")
stime = time.time()
try:
	inputs = [sympy.sympify(i, rational = True) for i in inputs]
except ValueError as E:
	print(E)
	exit()

if len(inputs) <= 1:
	print("More than one number is required")
	exit()

uni = {}
uni["diff_0"], v, uni["d0"] = difference(inputs)
formula = f"({inputs[0]}) + ({uni['d0']})*(n - 1)"
z = 1

while not v:
	uni["diff_"+str(z)], v, uni["d"+str(z)] = difference(uni["diff_"+str(z-1)])
	formula = create(z, formula, uni["d"+str(z)])
	z += 1

expand = sympy.expand(formula)
sympify = sympy.sympify(formula, rational = True)
factor = sympy.factor(formula)

if S:
	SFormula = f"n*(({inputs[0]}) + ({formula}))/2"
	
	SExpand = sympy.expand(SFormula)
	SSympify = sympy.sympify(SFormula, rational = True)
	SFactor = sympy.factor(SFormula)

print("\nFirst 50 elements of the pattern above:")
for n in range(1, 51):
	print(factor.subs("n", n), end=", ")

print("\n")

for i in range(z):
	if i == 0:
		pos = "1st"
	elif i == 1:
		pos = "2nd"
	elif i == 2:
		pos = "3rd"
	else:
		pos = str(i + 1) + "th"
	print(pos + " difference:")
	for j in uni["diff_" + str(i)]:
		print(j, end = ", ")
	print()

print("\nFactor:\n" + str(factor))
if S: print(str(SFactor))
print("Expand:\n" + str(expand))
if S: print(str(SExpand))
print("Sympify:\n" + str(sympify))
if S: print(str(SSympify))
print("\nFinished in " + str(time.time() - stime) + " seconds")