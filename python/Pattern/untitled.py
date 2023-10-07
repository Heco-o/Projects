import argparse
import threading
import time

stime = time.time()
run = threading.Event()
run.set()
animation = ["Please wait    ", "Please wait.   ", "Please wait..  ", "Please wait... ", "Please wait...."]
def animate():
	index = 0
	while run.is_set() and threading.main_thread().is_alive():
		print(animation[index % len(animation)], end="\r")
		index += 1
		time.sleep(0.2)

animate = threading.Thread(target=animate)
animate.start()
parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store_true", help="Formula for the sum of the nth term sequence")
parser.add_argument("-d", action="store_true", help="Approximation formula instead of the exact one")
_S = parser.parse_args().s
_D = parser.parse_args().d

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

def SCreate(n, x, d):
	facto = 2
	temp = "(n - 1)"
	for i in range(2, n + 2):
		temp += f"*(n - {i})"
		facto *= (i+1)
	return f"({x}) + ({d})*n*({temp})/{facto}"

run.clear()
animate.join()

print("\nDone! " + str(time.time() - stime) + " seconds\n")

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

uni = {"diff_-1": inputs.copy()}
formula = f"({inputs[0]})"
v, z = False, 0

if _S:
	SFormula = f"{inputs[0]}*n"
	while not v:
		uni["diff_"+str(z)], v, uni["d"+str(z)] = difference(uni["diff_"+str(z-1)])
		formula = create(z, formula, uni["d"+str(z)])
		SFormula = SCreate(z, SFormula, uni["d"+str(z)])
		z += 1
else:
	while not v:
		uni["diff_"+str(z)], v, uni["d"+str(z)] = difference(uni["diff_"+str(z-1)])
		formula = create(z, formula, uni["d"+str(z)])
		z += 1

expand = sympy.expand(formula)
sympify = sympy.sympify(formula, rational = True)
factor = sympy.factor(formula)

if _S:
	SExpand = sympy.expand(SFormula)
	SSympify = sympy.sympify(SFormula, rational = True)
	SFactor = sympy.factor(SFormula)

print("\nFirst 50 elements of the pattern above:")
if _D:
	for n in range(1, 51):
		print(factor.evalf(subs={"n": n}), end=", ")
else:
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
	if _D:
		for j in uni["diff_" + str(i)]:
			print(j.evalf(), end = ", ")
	else:
		for j in uni["diff_" + str(i)]:
			print(j, end = ", ")
	print()

if _D:
	print("\nFactor:\n" + str(factor.evalf()))
	if _S: print(str(SFactor.evalf()))
	print("Expand:\n" + str(expand.evalf()))
	if _S: print(str(SExpand.evalf()))
	print("Sympify:\n" + str(sympify.evalf()))
	if _S: print(str(SSympify.evalf()))
	print("\nFinished in " + str(time.time() - stime) + " seconds")
else:
	print("\nFactor:\n" + str(factor))
	if _S: print(str(SFactor))
	print("Expand:\n" + str(expand))
	if _S: print(str(SExpand))
	print("Sympify:\n" + str(sympify))
	if _S: print(str(SSympify))
	print("\nFinished in " + str(time.time() - stime) + " seconds")