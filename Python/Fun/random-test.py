import random
def test1():
	a = {}
	while True:
		b = random.randint(0, 9)
		try:
			a[b] += 1
		except KeyError:
			a[b] = 1
		print(a, end = "\r")
def test2():
	n = 9
	a = {}
	z = [i for i in range(n)]
	while True:
		random.shuffle(z)
		for i in range(n):
			try:
				a[z[i]] += i
			except KeyError:
				a[z[i]] = i
		print(a, end = "\r")

test2()