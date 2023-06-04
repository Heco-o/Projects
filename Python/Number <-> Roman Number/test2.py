keys = [1000000, 900000, 500000, 400000, 100000, 90000, 50000, 40000, 10000, 9000, 5000, 4000, 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 3, 2, 1]
values = ["M̅", "C̅M̅", "D̅", "C̅D̅", "C̅", "X̅C̅", "L̅", "X̅L̅", "X̅", "MX̅", "V̅", "MV̅", "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "III", "II", "I"]

def numToRoman(num):
	roman = ""
	while num != 0:
		for i, j in zip(keys, values):
			if num >= i:
				num -= i
				roman += j
				break
	return roman

def romanToNum(roman):
	roman = list(roman)
	
	for i in range(len(roman)):
		if roman[i] == "̅":
			roman[i - 1] = roman[i - 1] + "̅"
			roman[i] = 0
	while 0 in roman:
		roman.remove(0)
	num = 0
	while len(roman) != 0:
		if len(roman) > 1 and roman[0] + roman[1] in values:
			num += keys[values.index(roman[0] + roman[1])]
			roman.pop(0)
			roman.pop(0)
		else:
			num += keys[values.index(roman[0])]
			roman.pop(0)
	return num

try:
	option = int(input("Chose a mode:\n1: Whole number to Roman numeral\n2: Roman numeral to whole number\n"))
except ValueError as E:
	print(E)
	print("Numbers only!")
	exit()

if option == 1:
	num = int(input("Enter the number:\n"))
	roman = numToRoman(num)
	print(roman)
elif option == 2:
	roman = input("Enter the roman numeral:\n").upper().replace("_", "̅")
	num = romanToNum(roman)
	print(num)