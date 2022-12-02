print("Please Wait....")

import sympy

def diff(x):
	d = []
	v = []
	for i in range(len(x) - 1):
		d.append(x[i + 1] - x[i])
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

inputs = []
temp = input("Enter a pattern:\n").split(" ")

if "" in temp:
	print("Numbers only")
	exit()
if len(temp) <= 1:
	print("More than one number is required")
	exit()

for i in temp:
	inputs.append(int(i))

del temp

a = inputs[0]
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
for n in range(1, 51):
	print(int(eval(formula)), end = " ")

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
	eval("print(diff_" + str(i) + ")")

print("\nFactor:\n" + formula)
print("Expand:\n" + test0)
print("Sympify:\n" + test1)