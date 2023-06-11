numbers = [i for i in range(47,100) if len(set(str(i**2) + str(i**3))) == 10]
print(numbers)
"""
numbers = []
for i in range(47,100):
	total = set(str(i**2) + str(i**3))
	if len(total) == 10:
		numbers.append(i)
print(numbers)
"""