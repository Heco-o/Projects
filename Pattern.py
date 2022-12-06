print("Please Wait....")

import subprocess
try:
	import sympy
except ModuleNotFoundError as E:
	print(E)
	down = input("To run this file you will need to download simply module\nDo you want to download sympy module? (Y/n)\n").lower()
	if down.startswith("y"):
		print("Downloading...")
		subprocess.run(["pip3", "install", "sympy"])
	else:
		print("You can download sympy module by pip in terminal, for example:\npip install sympy\nor\npip3 install sympy")
	exit()
import decimal

def diff(x):
	d = []
	v = []
	if ints:
		for i in range(len(x) - 1):
			d.append(x[i + 1] - x[i])
	else:
		for i in range(len(x) - 1):
			d.append(sympy.Rational(str(float(decimal.Decimal(str(eval(str(x[i + 1])))) - decimal.Decimal(str(eval(str(x[i]))))))))
	for i in range(len(d) - 1):
		if d[i] == d[i + 1]:
			v.append(True)
		else:
			v.append(False)
	if False in v:
		return d.copy(), False, d[0]
	else:
		return d.copy(), True, d[0]

def create(n, x, d):
	f = 1
	t = "(n - 1)"
	for i in range(2, n + 1):
		t += " * (n - " + str(i) + ")"
		f *= i
	return x + " + " + "(" + str(d) + " * " + t + ") / " + str(f)

print("Done!\n")

ints = True
inputs = []
temp = input("Enter a pattern:\n").split(" ")

if len(temp) <= 1:
	print("More than one number is required")
	exit()

try:
	for i in temp:
		float(i)
		if type(eval(i)) == float:
			ints = False
		inputs.append(eval(i))
except ValueError:
	print("Number only")
	exit()

del temp

if ints:
	a = inputs[0]
else:
	a = sympy.Rational(str(inputs[0]))
diff_1, v, d1 = diff(inputs)
formula = str(a) + " + " + str(d1) + " * (n - 1)"
z = 1

while not v:
	exec("diff_" + str(z + 1) + ", v, d" + str(z + 1) + " = diff(diff_" + str(z) + ")")
	formula = create(z + 1, formula, eval("d" + str(z + 1)))
	z += 1

test0 = str(sympy.expand(formula))
test1 = str(sympy.sympify(formula, rational = True))

formula = str(sympy.factor(formula))

print("\nFirst 50 elements of the pattern above:")
if ints:
	for n in range(1, 51):
		print(int(eval(formula)), end = " ")
else:
	for n in range(1, 51):
		print(eval(formula), end = " ")

print("\n")

for i in range(1, z + 1):
	if i == 1:
		pos = "1st"
	elif i == 2:
		pos = "2nd"
	elif i == 3:
		pos = "3rd"
	else:
		pos = str(i) + "th"
	print(pos + " difference:")
	for j in eval("diff_" + str(i)):
		print(eval(str(j)), end = " ")
	print()

print("\nFactor:\n" + formula)
print("Expand:\n" + test0)
print("Sympify:\n" + test1)
