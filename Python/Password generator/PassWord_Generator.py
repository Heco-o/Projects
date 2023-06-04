def passgen():
	from random import choice, shuffle; from os.path import exists, isdir; a = ["0","1","2","3","4","5","6","7","8","9"]; b = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]; c = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]; d = ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","+","=","{","[","}","]","|","\\",":",";","\"","'","<",",",">",".","?","/"]; passwords = []; global generate; key0 = False; key1 = False; returns = ""
	def _generate(t):
		while True:
			global generate
			generate = input(f"[{t}] How many passwords do you want to generate? [Tip: Just pressing Enter will generate one password]\n")
			if generate == "": generate = 1; break
			if generate.isdigit() == False: print(f"[{t}] Please enter only numbers or just press Enter to generate one password\n"); continue
			generate = int(generate)
			if generate <= 0: print(f"[{t}] Please enter only numbers that are larger than 0 or just press Enter to generate one password\n"); continue
			break
	def _lenth(t, p = ""):
		while True:
			l = input(f"[{t}]{p} How many characters do you want in your password?\n")
			if l.isdigit() == False: print(f"[{t}]{p} Please enter only numbers that are larger than 0\n"); continue
			if int(l) <= 0: print(f"[{t}]{p} Please enter only numbers that are larger than 0\n"); continue
			l = int(l); break
		return l
	def _input(t, p = ""):
		while True:
			A = []
			n = input(f"[{t}]{p} Do you want any numbers in your password? Y/N\n").lower()
			u = input(f"[{t}]{p} Do you want any uppercase letters in your password? Y/N\n").lower()
			l = input(f"[{t}]{p} Do you want any lowercase letters in your password? Y/N\n").lower()
			s = input(f"[{t}]{p} Do you want any special characters in your password? Y/N\n").lower()
			if n.startswith("y") or u.startswith("y") or l.startswith("y") or s.startswith("y"): break
			print(f"[{t}]{p} Please at least choose one of the options\n")
		if n.startswith("y"): [A.append(i) for i in a]
		if u.startswith("y"): [A.append(i) for i in c]
		if l.startswith("y"): [A.append(i) for i in b]
		if s.startswith("y"): [A.append(i) for i in d]
		return A
	def _exclude(A, t, p = ""):
		e = input(f"[{t}]{p} Do you want to exclude any letters, numbers or symbols? Y/N\n")
		if e.startswith("y"):
			while True:
				c = []
				print(f"[{t}]{p} What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any spaces between them)\n")
				A.sort()
				for i in A: print(i, end = " ")
				r = input("\n\n")
				if r == "": break
				for i in r: print(f"[{t}]{p} Please enter only valid symbols, numbers or letters or just press enter to exclude nothing\n") if not i in A else None; e = True if not i in A else None; c.append(i)
				if e: continue
				if A == c: print(f"[{t}]{p} You can't exclude everything\n"); continue
				if " " in r: print(f"[{t}]{p} Please do NOT enter any spaces\n"); continue
				for i in r: A.remove(i)
				break
	def normal():
		A = []
		tag = "Normal"
		_generate(tag)
		lenth = _lenth(tag)
		A = _input(tag)
		_exclude(A, tag)
		for i in range(generate): password = ""; [[shuffle(A), B := choice(A), password := password + B] for i in range(lenth)]; passwords.append(password)
	def full():
		tag = "Full"
		place = 0
		_generate(tag)
		option = input("[Full] Do you want to choose options for each of your passwords? Y/N\n").lower() if generate > 1 else ""; options = True if option.startswith("y") else False
		if not options:
			A = []
			lenth = _lenth(tag)
			A = _input(tag)
			_exclude(A, tag)
			for i in range(generate): password = ""; [[shuffle(A), B := choice(A), password := password + B] for i in range(lenth)]; passwords.append(password)
		else:
			A = []
			for i in range(generate):
				place += 1
				position = " 1st password:" if place == 1 else " 2nd password:" if place == 2 else " 3rd password:" if place == 3 else f" {place}th password:"
				lenth = _lenth(tag, position)
				A = _input(tag, position)
				_exclude(A, tag, position)
				password = ""; [[shuffle(A), B := choice(A), password := password + B] for i in range(lenth)]; passwords.append(password)
	def custom():
		tag = "Custom"
		A = []
		place = 0
		while True:
			key0 = True
			custom = ""
			print('[Custom] Please enter symbols, numbers, or letters that will be used to generate passwords (please do NOT put any spaces between them)\n[Enter "nums" to add the default numbers; "syms" to add the default special characters; "lows" to add the default lowercase letters; "ups" to add the default uppercase letters; "def" to add all the default letters, numbers, and symbols; and "cl" to clear what you\'ve added; make sure to enter everything in lowercase]\n[Just press enter when you\'re done]\n')
			for i in A: print(i, end = " ")
			print("\n")
			custom = input()
			print("\n")
			[[A.append(i) for i in a + b + c + d], key0 := False] if custom == "def" else [[A.append(i) for i in a], key0 := False] if custom == "nums" else [[A.append(i) for i in d], key0 := False] if custom == "syms" else [[A.append(i) for i in b], key0 := False] if custom == "lows" else [[A.append(i) for i in c], key0 := False] if custom == "ups" else [A.clear(), key0 := False] if custom == "cl" else [[A.append(i) for i in custom], key0 := False] if custom != "" and not " " in custom else [print("[Custom] Please do NOT enter any spaces\n"), key0 := False] if " " in custom else [print("[Custom] Please enter at least one symbol, number or letter\n"), key0 := False] if A == [] else ""
			if key0: break
		_generate(tag)
		option = input("[Custom] Do you want to choose options for each of your passwords? Y/N\n").lower() if generate > 1 else ""; options = True if option.startswith("y") else False
		if not options:
			lenth = _lenth(tag)
			_exclude(A, tag)
			for i in range(generate): password = ""; [[shuffle(A), B := choice(A), password := password + B] for i in range(lenth)]; passwords.append(password)
		else:
			for i in range(generate):
				place += 1
				position = " 1st password:" if place == 1 else " 2nd password:" if place == 2 else " 3rd password:" if place == 3 else f" {place}th password:"
				borrow = A.copy()
				lenth = _lenth(tag, position)
				_exclude(borrow, tag, position)
				password = ""; [[shuffle(borrow), B := choice(borrow), password := password + B] for i in range(lenth)]; passwords.append(password)
	while True:
		choose = input("Choose one\nMode: Normal(N), Full(F), Custom(C)\n").lower()
		[normal(), key1 := True] if choose.startswith("n") else [full(), key1 := True] if choose.startswith("f") else [custom(), key1 := True] if choose.startswith("c") else print("Please choose a valid Mode\n")
		if key1: break
	
	print(passwords)
passgen()