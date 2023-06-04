def sort(_list):
	highest = _list[0]
	for i in range(len(_list) - 1):
		if highest < _list[i + 1]:
			highest = _list[i + 1]
		

numbers = [5, 18, 23, 12, 2, 3, 1, 8,6,9,21,24]
print(numbers)