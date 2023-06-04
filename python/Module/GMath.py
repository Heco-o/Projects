def __zeros(a):
	if "-" in a[0]:
		minus = True
		a[0] = a[0].replace("-", "")
	else:
		minus = False
	while len(a[0]) > 0 and a[0][0] == "0":
		a[0] = a[0][1:]
	if len(a[0]) == 0:
		a[0] = a[1]
		while len(a[0]) > 0 and a[0][0] == "0":
			a[0] = a[0][1:]
		if len(a[0]) == 0:
			a[0] = "0"
			a[1] = ""
			return a.copy()
		a[0] = a[0] + "#"
	while len(a[1]) > 0 and a[1][-1] == "0":
		a[1] = a[1][:-1]
	if minus:
		a[0] = "-" + a[0]
	return a.copy()

def add(a, b):
	float(a); a = str(a)
	float(b); b = str(b)

def optimise(a, b):
	float(a); a = str(a)
	float(b); b = str(b)
	if not "." in a: a = a + ".0"
	if not "." in b: b = b + ".0"
	a, afterPointA = __zeros(a.split(".").copy())
	b, afterPointB = __zeros(b.split(".").copy())
	if any([False if i == "0" else True for i in afterPointA]) or any([False if i == "0" else True for i in afterPointB]):
		if len(afterPointA) == len(afterPointB):
			if "#" in a and "#" in b:
				a = a.replace("#", "")
				b = b.replace("#", "")
			elif "#" in a:
				a = a.replace("#", "")
				b += afterPointB
			elif "#" in b:
				a += afterPointA
				b = b.replace("#", "")
			else:
				a += afterPointA
				b += afterPointB
		elif len(afterPointA) > len(afterPointB):
			if "#" in a and "#" in b:
				a = a.replace("#", "")
				b = b.replace("#", "") + "0" * (len(afterPointA) - len(afterPointB))
			elif "#" in a:
				a = a.replace("#", "")
				b += afterPointB + "0" * (len(afterPointA) - len(afterPointB)) if not(afterPointB == "" and b == "0") else ""
			elif "#" in b:
				a += afterPointA
				b = b.replace("#", "") + "0" * (len(afterPointA) - len(afterPointB))
			else:
				a += afterPointA
				b += afterPointB + "0" * (len(afterPointA) - len(afterPointB)) if not(afterPointB == "" and b == "0") else ""
		elif len(afterPointA) < len(afterPointB):
			if "#" in a and "#" in b:
				a = a.replace("#", "") + "0" * (len(afterPointB) - len(afterPointA))
				b = b.replace("#", "")
			elif "#" in a:
				a = a.replace("#", "") + "0" * (len(afterPointB) - len(afterPointA))
				b += afterPointB
			elif "#" in b:
				a += afterPointA + "0" * (len(afterPointB) - len(afterPointA)) if not(afterPointA == "" and a == "0") else ""
				b = b.replace("#", "")
			else:
				a += afterPointA + "0" * (len(afterPointB) - len(afterPointA)) if not(afterPointA == "" and a == "0") else ""
				b += afterPointB
	return a, b

def division(a, b, L=16, Round=True):
	a, b = optimise(a, b)
	if a == "0" or b == "0":
		return "0"
	if a == b:
		return "1"
	if "-" in a:
		a = a.replace("-", "")
		asee = True
	else: asee = False
	if "-" in b:
		b = b.replace("-", "")
		bsee = True
	else: bsee = False
	if asee ^ bsee: state = True
	else: state = False
	if a == b and state:
		return "-1"
	if L == 0 and int(a) < int(b):
		return "0"
	elif int(a) < int(b):
		result = "0."
		a += "0"
	else: result = ""
	while L != 0 and int(a) < int(b):
		result += "0"
		a += "0"
		L -= 1
	if L == 0 and int(a) < int(b):
		return "-" + result if state else result
	if not "." in result:
		result += str(int((int(a) - (int(a) % int(b))) / int(b)))
		if int(a) % int(b) != 0:
			result += "." if L != 0 else ""
			a = str(int(a) % int(b)) + "0"
	if "." in result:
		while L != 0:
			result += str(int((int(a) - (int(a) % int(b))) / int(b)))
			if int(a) % int(b) == 0:
				break
			a = str(int(a) % int(b)) + "0"
			L -= 1
			while L != 0 and int(a) < int(b):
				result += "0"
				a += "0"
				L -= 1
	return "-" + result if state else result
def differential(x, module=False, fun=False, checkSimilarity=False, negetive=True):
	if module == False and fun == False:
		from decimal import Decimal
		if negetive:
			d = [(float(Decimal(str(x[i + 1])) - Decimal(str(x[i])))) for i in range(len(x) - 1)]
		else:
			d = [(abs(float(Decimal(str(x[i + 1])) - Decimal(str(x[i]))))) for i in range(len(x) - 1)]
		if checkSimilarity:
			v = all([(True if d[i + 1] == d[i] else False) for i in range(len(d) - 1)])
			return d.copy(), v
		return d.copy()

if __name__ == '__main__':
	get = int(input("1. optimise\n2. division\n3. differential\n"))
	if get == 1:
		x = input("Input the first number:\n")
		y = input("Input the second number:\n")
		x, y = optimise(x, y)
		print("\n" + x)
		print(y)
	elif get == 2:
		x = input("Input the first number:\n")
		y = input("Input the second number:\n")
		z = division(x, y)
		print("\n" + z)
	elif get == 3:
		x = input("Input the numbers:\n").split(",")
		z = differential(x, checkSimilarity=True, negetive=False)
		print(z)