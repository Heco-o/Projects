def sort(_list):
	for i in range(len(_list) - 1):
		for j in range(len(_list) - i - 1):
			if _list[i] > _list[i+j+1]:
				_list[i], _list[i+j+1] = _list[i+j+1], _list[i]

numbers = [5, 18, 23, 12, 2, 3, 1, 8, 6, 9, 21, 5, 24]
sort(numbers)
print(numbers)