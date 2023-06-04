import time, threading
emit = time.time()
NotDone = True
def load():
	animation = ["Please wait    ", "Please wait.   ", "Please wait..  ", "Please wait... ", "Please wait...."]
	inx = 0
	while NotDone:
		print(animation[inx % 5], end = "\r")
		inx += 1
		time.sleep(0.2)
load = threading.Thread(target = load)
load.start()

import subprocess
try:
	import sympy
except ModuleNotFoundError as E:
	NotDone = False
	del load
	print()
	print(E)
	down = input("To run this file you will need to download simpy module\nDo you want to download sympy module? (Y/n)\n").lower()
	if down.startswith("y"):
		print("Downloading...")
		subprocess.run(["pip3", "install", "sympy"])
	else:
		print("You can download sympy module by pip in terminal, for example:\npip install sympy\nor\npip3 install sympy")
	exit()
import decimal

del subprocess

def pattern(x, d):
	l = [d]
	if ints:
		for i in x:
			d += i
			l.append(d)
	else:
		for i in x:
			d = float(decimal.Decimal(str(d)) + decimal.Decimal(str(i)))
			l.append(d)
	return l.copy()

def create(n, x, d):
	f = 1
	t = "(n - 1)"
	for i in range(2, n + 1):
		t += " * (n - " + str(i) + ")"
		f *= i
	return x + " + " + "(" + str(d) + " * " + t + ") / " + str(f)

NotDone = False
del load, threading
print("\nDone!")
print("Done in " + str(time.time() - emit) + " seconds\n")

z = 0
ints = True
inputs = []

temp0 = input("Enter the first number of the pattern:\n")

try:
	float(temp0)
except ValueError:
	print("Number only")
	exit()

if type(eval(temp0)) == float:
	ints = False

temp = input("\nEnter the first differences of each row of the pattern:\n").split(" ")

emit = time.time()

temp.insert(0, temp0)

try:
	for i in temp:
		float(i)
		if type(eval(i)) == float:
			ints = False
		inputs.append(eval(i))
except ValueError:
	print("Number only")
	exit()

del temp, temp0

if ints:
	del decimal
	a = inputs[0]
	b = inputs[1]
else:
	a = sympy.Rational(str(inputs[0]))
	b = sympy.Rational(str(inputs[1]))
formula = str(a) + " + " + str(b) + " * (n - 1)"

diff_1 = [inputs[-1], inputs[-1], inputs[-1], inputs[-1]]
if len(inputs) > 2:
	D2l = [pattern(diff_1.copy(), inputs[-2]), diff_1.copy()]
else:
	D2l = [diff_1.copy()]

for i in range(2, len(inputs) - 1):
	D2l.insert(0, pattern(D2l[-i], inputs[-i - 1]))

for i in range(2, len(inputs)):
	formula = create(i, formula, sympy.Rational(str(inputs[i])))

test0 = str(sympy.expand(formula))
test1 = str(sympy.sympify(formula, rational = True))

formula = str(sympy.factor(formula))

emit = time.time() - emit

print("\nFirst 50 elements with the differences above:")
if ints:
	for n in range(1, 51):
		print(int(eval(formula)), end = " ")
else:
	for n in range(1, 51):
		print(eval(formula), end = " ")

print("\n")

for i in D2l:
	z += 1
	if z == 1:
		pos = "1st"
	elif z == 2:
		pos = "2nd"
	elif z == 3:
		pos = "3rd"
	else:
		pos = str(z) + "th"
	print(pos + " difference:")
	for j in i:
		print(j, end = " ")
	print()

print("\nFactor:\n" + formula)
print("Expand:\n" + test0)
print("Sympify:\n" + test1)
print("\nDone in " + str(emit) + " seconds")