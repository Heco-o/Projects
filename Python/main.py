import GMath
import random
num = 0
for i in range(100000):
	x = random.randint(-999999, 999999)
	y = random.randint(-999999, 999999)
	a = str(x / y)
	if "e" in a:
		num += 1
		continue
	b = GMath.division(x, y, 16)
	a = a[:-2]
	b = b[:-2]
	if len(a) > len(b):
		a = a[:len(b) - len(a)]
	if len(b) > len(a):
		b = b[:len(a) - len(b)]
	if a != b:
		break
if a != b:
	print(a)
	print(b)
	print(x)
	print(y)
print(num)