def sort0(x):
	for i in range(len(x) - 1):
		for j in range(len(x) - i - 1):
			if x[i] > x[i+j+1]:
				x[i], x[i+j+1] = x[i+j+1], x[i]

def sort1(x):
	for i in range(len(x) - 1):
		for j in range(len(x) - 1):
			if x[j] > x[j+1]:
				x[j], x[j+1] = x[j+1], x[j]

numbers = [5, 18, 23, 12, 2, 3, 1, 8, 6, 9, 21, 5, 24]
#print(numbers)
sort1(numbers)
print(numbers)