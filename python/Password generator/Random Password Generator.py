def passgen():
	from random import choice, shuffle
	from os.path import exists, isdir
	a = ["0","1","2","3","4","5","6","7","8","9"]
	b = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	c = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	d = ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","+","=","{","[","}","]","|","\\",":",";","\"","'","<",",",">",".","?","/"]
	passwords = []
	generate = ""
	key0 = False
	def normal():
		A = []
		while True:
			try:
				generate = input("[Normal] How many passwords do you want to generate? [Tip: Just pressing Enter will generate one password]\n")
				generate = int(generate)
				if generate <= 0:
					print("[Normal] Please enter only numbers that are larger than 0 or just press Enter to generate one password\n")
				else:
					break
			except ValueError:
				if generate == "":
					generate = 1
					break
				else:
					print("[Normal] Please enter only numbers or just press Enter to generate one password\n")
		while True:
			try:
				lenth = int(input("[Normal] How many characters do you want in your password?\n"))
				if lenth <= 0:
					print("[Normal] Please enter only numbers that are larger than 0\n")
				else:
					break
			except ValueError:
				print("[Normal] Please enter only numbers\n")
		while True:
			number = input("[Normal] Do you want any numbers in your password? Y/N\n").lower()
			uppercase = input("[Normal] Do you want any uppercase letters in your password? Y/N\n").lower()
			lowercase = input("[Normal] Do you want any lowercase letters in your password? Y/N\n").lower()
			special = input("[Normal] Do you want any special characters in your password? Y/N\n").lower()
			if number == "yes" or number == "y" or number.startswith("y") or uppercase == "yes" or uppercase == "y" or uppercase.startswith("y") or lowercase == "yes" or lowercase == "y" or lowercase.startswith("y") or special == "yes" or special == "y" or special.startswith("y"):
				break
			else:
				print("[Normal] Please at least choose one of the options\n")
		if number == "yes" or number == "y" or number.startswith("y"):
			for i in a:
				A.append(i)
		if uppercase == "yes" or uppercase == "y" or uppercase.startswith("y"):
			for i in c:
				A.append(i)
		if lowercase == "yes" or lowercase == "y" or lowercase.startswith("y"):
			for i in b:
				A.append(i)
		if special == "yes" or special == "y" or special.startswith("y"):
			for i in d:
				A.append(i)
		exclude = input("[Normal] Do you want to exclude any letters, numbers or symbols? Y/N\n")
		if exclude == "yes" or exclude == "y" or exclude.startswith("y"):
			recovery = ""
			while True:
				try:
					print("[Normal] What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any spaces between them)\n")
					A.sort()
					for i in A:
						print(i, end = " ")
					remove = input("\n\n")
					for i in remove:
						A.remove(i)
						recovery += i
					if A == []:
						for i in recovery:
							A.append(i)
							recovery = ""
						print("[Normal] You can't exclude everything\n")
						continue
					break
				except ValueError:
					if recovery != "":
						for i in recovery:
							A.append(i)
							recovery = ""
					if remove == "":
						break
					else:
						print("[Normal] Please enter only valid symbols, numbers or letters or just press enter to exclude nothing\n")
		for i in range(generate):
			password = ""
			for i in range(lenth):
				shuffle(A)
				B = choice(A)
				password += B
			passwords.append(password)
	def full():
		option = ""
		place = 0
		while True:
			try:
				generate = input("[Full] How many passwords do you want to generate? [Tip: Just pressing Enter will generate one password]\n")
				generate = int(generate)
				if generate <= 0:
					print("[Full] Please enter only numbers that are larger than 0 or just press Enter to generate one password\n")
				else:
					break
			except ValueError:
				if generate == "":
					generate = 1
					break
				else:
					print("[Full] Please enter only numbers or just press Enter to generate one password\n")
		if generate > 1:
			option = input("[Full] Do you want to choose options for each of your passwords? Y/N\n").lower()
		if option == "yes" or option == "y" or option.startswith("y"):
			options = True
		else:
			options = False
		if not options:
			A = []
			while True:
				try:
					lenth = int(input("[Full] How many characters do you want in your password?\n"))
					if lenth <= 0:
						print("[Full] Please enter only numbers that are larger than 0\n")
					else:
						break
				except ValueError:
					print("[Full] Please enter only numbers\n")
			while True:
				number = input("[Full] Do you want any numbers in your password? Y/N\n").lower()
				uppercase = input("[Full] Do you want any uppercase letters in your password? Y/N\n").lower()
				lowercase = input("[Full] Do you want any lowercase letters in your password? Y/N\n").lower()
				special = input("[Full] Do you want any special characters in your password? Y/N\n").lower()
				if number == "yes" or number == "y" or number.startswith("y") or uppercase == "yes" or uppercase == "y" or uppercase.startswith("y") or lowercase == "yes" or lowercase == "y" or lowercase.startswith("y") or special == "yes" or special == "y" or special.startswith("y"):
					break
				else:
					print("[Full] Please at least choose one of the options\n")
			if number == "yes" or number == "y" or number.startswith("y"):
				for i in a:
					A.append(i)
			if uppercase == "yes" or uppercase == "y" or uppercase.startswith("y"):
				for i in c:
					A.append(i)
			if lowercase == "yes" or lowercase == "y" or lowercase.startswith("y"):
				for i in b:
					A.append(i)
			if special == "yes" or special == "y" or special.startswith("y"):
				for i in d:
					A.append(i)
			exclude = input("[Full] Do you want to exclude any letters, numbers or symbols? Y/N\n")
			if exclude == "yes" or exclude == "y" or exclude.startswith("y"):
				recovery = ""
				while True:
					try:
						print("[Full] What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any spaces between them)\n")
						A.sort()
						for i in A:
							print(i, end = " ")
						remove = input("\n\n")
						for i in remove:
							A.remove(i)
							recovery += i
						if A == []:
							for i in recovery:
								A.append(i)
								recovery = ""
							print("[Full] You can't exclude everything\n")
							continue
						break
					except ValueError:
						if recovery != "":
							for i in recovery:
								A.append(i)
								recovery = ""
						if remove == "":
							break
						else:
							print("[Full] Please enter only valid symbols, numbers or letters or just press enter to exclude nothing\n")
			for i in range(generate):
				password = ""
				for i in range(lenth):
					shuffle(A)
					B = choice(A)
					password += B
				passwords.append(password)
		else:
			for i in range(generate):
				place += 1
				if place == 1:
					position = "1st"
				elif place == 2:
					position = "2nd"
				elif place == 3:
					position = "3rd"
				else:
					position = f"{place}th"
				A = []
				while True:
					try:
						lenth = int(input(f"[Full] {position} password: How many characters do you want in your password?\n"))
						if lenth <= 0:
							print(f"[Full] {position} password: Please enter only numbers that are larger than 0\n")
						else:
							break
					except ValueError:
						print(f"[Full] {position} password: Please enter only numbers\n")
				while True:
					number = input(f"[Full] {position} password: Do you want any numbers in your password? Y/N\n").lower()
					uppercase = input(f"[Full] {position} password: Do you want any uppercase letters in your password? Y/N\n").lower()
					lowercase = input(f"[Full] {position} password: Do you want any lowercase letters in your password? Y/N\n").lower()
					special = input(f"[Full] {position} password: Do you want any special characters in your password? Y/N\n").lower()
					if number == "yes" or number == "y" or number.startswith("y") or uppercase == "yes" or uppercase == "y" or uppercase.startswith("y") or lowercase == "yes" or lowercase == "y" or lowercase.startswith("y") or special == "yes" or special == "y" or special.startswith("y"):
						break
					else:
						print(f"[Full] {position} password: Please at least choose one of the options\n")
				if number == "yes" or number == "y" or number.startswith("y"):
					for i in a:
						A.append(i)
				if uppercase == "yes" or uppercase == "y" or uppercase.startswith("y"):
					for i in c:
						A.append(i)
				if lowercase == "yes" or lowercase == "y" or lowercase.startswith("y"):
					for i in b:
						A.append(i)
				if special == "yes" or special == "y" or special.startswith("y"):
					for i in d:
						A.append(i)
				exclude = input(f"[Full] {position} password: Do you want to exclude any letters, numbers or symbols? Y/N\n")
				if exclude == "yes" or exclude == "y" or exclude.startswith("y"):
					recovery = ""
					while True:
						try:
							print(f"[Full] {position} password: What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any spaces between them)\n")
							A.sort()
							for i in A:
								print(i, end = " ")
							remove = input("\n\n")
							for i in remove:
								A.remove(i)
								recovery += i
							if A == []:
								for i in recovery:
									A.append(i)
									recovery = ""
								print("[Full] You can't exclude everything\n")
								continue
							break
						except ValueError:
							if recovery != "":
								for i in recovery:
									A.append(i)
								recovery = ""
							if remove == "":
								break
							else:
								print("[Full] {position} password: Please enter only valid symbols, numbers or letters or just press enter to exclude nothing\n")
				password = ""
				for i in range(lenth):
					shuffle(A)
					B = choice(A)
					password += B
				passwords.append(password)
	def custom():
		A = []
		option = ""
		place = 0
		while True:
			custom = ""
			print('[Custom] Please enter symbols, numbers, or letters that will be used to generate passwords (please do NOT put any spaces between them)\n[Enter "nums" to add the default numbers; "syms" to add the default special characters; "lows" to add the default lowercase letters; "ups" to add the default uppercase letters; "def" to add all the default letters, numbers, and symbols; and "cl" to clear what you\'ve added; make sure to enter everything in lowercase]\n[Just press enter when you\'re done]\n')
			for i in A:
				print(i, end = " ")
			print("\n")
			custom = input()
			print("\n")
			if custom == "def":
				for i in a:
					A.append(i)
				for i in b:
					A.append(i)
				for i in c:
					A.append(i)
				for i in d:
					A.append(i)
			elif custom == "nums":
				for i in a:
					A.append(i)
			elif custom == "syms":
				for i in d:
					A.append(i)
			elif custom == "lows":
				for i in b:
					A.append(i)
			elif custom == "ups":
				for i in c:
					A.append(i)
			elif custom == "cl":
				A.clear()
			elif custom != "" and not " " in custom:
				for i in custom:
					A.append(i)
			elif " " in custom:
				print("[Custom] Please do NOT enter any spaces\n")
			elif A == []:
				print("[Custom] Please enter at least one symbol, number or letter\n")
			else:
				break
		while True:
			try:
				generate = input("[Custom]  How many passwords do you want to generate? [Tip: Just pressing Enter will generate one password]\n")
				generate = int(generate)
				if generate <= 0:
					print("[Custom] Please enter only numbers that are larger than 0 or just press Enter to generate one password\n")
				else:
					break
			except ValueError:
				if generate == "":
					generate = 1
					break
				else:
					print("[Custom] Please enter only numbers or just press Enter to generate one password\n")
		if generate > 1:
			option = input("[Custom] Do you want to choose options for each of your passwords? Y/N\n").lower()
		if option == "yes" or option == "y" or option.startswith("y"):
			options = True
		else:
			options = False
		if not options:
			while True:
				try:
					lenth = int(input("[Custom] How many characters do you want in your password?\n"))
					if lenth <= 0:
						print("[Custom] Please enter only numbers that are larger than 0\n")
					else:
						break
				except ValueError:
					print("[Custom] Please enter only numbers\n")
			exclude = input("[Custom] Do you want to exclude any letters, numbers or symbols? Y/N\n")
			if exclude == "yes" or exclude == "y" or exclude.startswith("y"):
				recovery = ""
				while True:
					try:
						print("[Custom] What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any spaces between them)\n")
						for i in A:
							print(i, end = " ")
						remove = input("\n\n")
						for i in remove:
							A.remove(i)
							recovery += i
						if A == []:
							for i in recovery:
								A.append(i)
								recovery = ""
							print("[Custom] You can't exclude everything\n")
							continue
						break
					except ValueError:
						if recovery != "":
							for i in recovery:
								A.append(i)
								recovery = ""
						if remove == "":
							break
						else:
							print("[Custom] Please enter only valid symbols, numbers or letters or just press enter to exclude nothing\n")
			for i in range(generate):
				password = ""
				for i in range(lenth):
					shuffle(A)
					B = choice(A)
					password += B
				passwords.append(password)
		else:
			for i in range(generate):
				place += 1
				if place == 1:
					position = "1st"
				elif place == 2:
					position = "2nd"
				elif place == 3:
					position = "3rd"
				else:
					position = f"{place}th"
				borrow = A.copy()
				while True:
					try:
						lenth = int(input(f"[Custom] {position} password: How many characters do you want in your password?\n"))
						if lenth <= 0:
							print(f"[Custom] {position} password: Please enter only numbers that are larger than 0\n")
						else:
							break
					except ValueError:
						print(f"[Custom] {position} password: Please enter only numbers\n")
				exclude = input(f"[Custom] {position} password: Do you want to exclude any letters, numbers or symbols? Y/N\n")
				if exclude == "yes" or exclude == "y" or exclude.startswith("y"):
					recovery = ""
					while True:
						try:
							print(f"[Custom] {position} password: What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any spaces between them)\n")
							borrow.sort()
							for i in borrow:
								print(i, end = " ")
							remove = input("\n\n")
							for i in remove:
								borrow.remove(i)
								recovery += i
							if borrow == []:
								for i in recovery:
									borrow.append(i)
									recovery = ""
								print("[Custom] You can't exclude everything\n")
								continue
							break
						except ValueError:
							if recovery != "":
								for i in recovery:
									borrow.append(i)
								recovery = ""
							if remove == "":
								break
							else:
								print("[Custom] {position} password: Please enter only valid symbols, numbers or letters or just press enter to exclude nothing\n")
				password = ""
				for i in range(lenth):
					shuffle(borrow)
					B = choice(borrow)
					password += B
				passwords.append(password)
	returns = ""
	while True:
		choose = input("Choose one\nMode: Normal(N), Full(F), Custom(C)\n").lower()
		if choose == "normal" or choose == "n" or choose.startswith("n"):
			normal()
			break
		elif choose == "full" or choose == "f" or choose.startswith("f"):
			full()
			break
		elif choose == "custom" or choose =="c" or choose.startswith("c"):
			custom()
			break
		else:
			print("Please choose a valid Mode\n")
	while True:
		returns = input('Do you want to Print(P) the passwords here or put in a File(F) or do Both(B) Print the passwords here and put the passwords in a file? [Tip: Just tapping enter will return the passwords from the "passgen()" function]\n').lower()
		if returns == "":
			return passwords
			break
		elif returns == "print" or returns == "p" or returns.startswith("p"):
			print("\nYour passwords are,\n\n")
			for i in passwords:
				print(f"{i}\n")
			break
		elif returns == "file" or returns == "f" or returns.startswith("f"):
			while True:
				write = input("Do you want to put the file in the current Poject(P) folder or in another Location(L)?\n").lower()
				if write == "project" or write == "p" or write.startswith("p"):
					name = input("Write the name of the file\n")
					if " " in name[0] or " " in name[-1] or "\\" in name or "/" in name:
						print("Please don't put any space at the beginning and end of the name, and don't put any \"\\\" or \"/\" in the name\n")
						continue
					elif exists(name) and isdir(name):
						print("A directory already exist with that name\n")
						continue
					elif exists(name):
						while True:
							overwrite = input("A file already exist with that name but do you want to Overwrite(O) it or Append(A) over it? [Tip: If you don't want to Overwrite or Append over it then just press enter]\n").lower()
							if overwrite == "overwrite" or overwrite == "o" or overwrite.startswith("o"):
								if len(passwords) > 1:
									backup = passwords[0]
									with open(name, "w") as file:
										file.write(passwords[0])
										passwords.pop(0)
									with open(name, "a") as file:
										for i in passwords:
											file.write(f"\n\n{i}")
									passwords.insert(0, backup)
									print("The File has Successfully Overwritten\n")
									key0 = True
									break
								elif len(passwords) == 1:
									with open(name, "w") as file:
										file.write(passwords[0])
									print("The File has Successfully Overwritten\n")
									key0 = True
									break
							elif overwrite == "append" or overwrite == "a" or overwrite.startswith("a"):
								if len(passwords) > 1:
									with open(name, "a") as file:
										for i in passwords:
											file.write(f"\n\n{i}")
									print("The File has Successfully Appended\n")
									key0 = True
									break
								elif len(passwords) == 1:
									with open(name, "a") as file:
										file.write("\n\n"+passwords[0])
									print("The File has Successfully Appended\n")
									key0 = True
									break
							elif overwrite == "":
								break
							else:
								print("Please enter a valid option or just press enter if you don't want to Overwrite or append over it\n")
					else:
						if len(passwords) > 1:
							backup = passwords[0]
							with open(name, "w") as file:
								file.write(passwords[0])
								passwords.pop(0)
							with open(name, "a") as file:
								for i in passwords:
									file.write(f"\n\n{i}")
							passwords.insert(0, backup)
							print("The File has Successfully Created\n")
							key0 = True
							break
						elif len(passwords) == 1:
							with open(name, "w") as file:
								file.write(passwords[0])
							print("The File has Successfully Created\n")
							key0 = True
							break
					if key0:
						break
				elif write == "location" or write == "l" or write.startswith("l"):
					while True:
						location = input("Please enter the Location you want to put the file in (Please make use to add \ or / add the end according to your device)\n")
						if not exists(location) and not isdir(location):
							print("Please enter a valid Location\n")
							continue
						elif location[-1] != "/" and location[-1] != "\\":
							print('Please add "\\" or "/" at the end according to your device\n')
							continue
						else:
							break
					while True:
						name = input("Please enter the name of the file\n")
						if " " in name[0] or " " in name[-1] or "\\" in name or "/" in name:
							print("Please don't put any space at the beginning and end of the name, and don't put any \"\\\" or \"/\" in the name\n")
							continue
						name = location + name
						if exists(name) and isdir(name):
							print("A directory already exist with that name\n")
							continue
						elif exists(name):
							while True:
								overwrite = input("A file already exist with that name but do you want to Overwrite(O) it or Append(A) over it? [Tip: If you don't want to Overwrite or Append over it then just press enter]\n").lower()
								if overwrite == "overwrite" or overwrite == "o" or overwrite.startswith("o"):
									if len(passwords) > 1:
										backup = passwords[0]
										with open(name, "w") as file:
											file.write(passwords[0])
											passwords.pop(0)
										with open(name, "a") as file:
											for i in passwords:
												file.write(f"\n\n{i}")
										passwords.insert(0, backup)
										print("The File has Successfully Overwritten\n")
										key0 = True
										break
									elif len(passwords) == 1:
										with open(name, "w") as file:
											file.write(passwords[0])
										print("The File has Successfully Overwritten\n")
										key0 = True
										break
								elif overwrite == "append" or overwrite == "a" or overwrite.startswith("a"):
									if len(passwords) > 1:
										with open(name, "a") as file:
											for i in passwords:
												file.write(f"\n\n{i}")
										print("The File has Successfully Appended\n")
										key0 = True
										break
									elif len(passwords) == 1:
										with open(name, "a") as file:
											file.write("\n\n"+passwords[0])
										print("The File has Successfully Appended\n")
										key0 = True
										break
								elif overwrite == "":
									break
								else:
									print("Please enter a valid option or just press enter if you don't want to Overwrite or append over it\n")
						else:
							if len(passwords) > 1:
								backup = passwords[0]
								with open(name, "w") as file:
									file.write(passwords[0])
									passwords.pop(0)
								with open(name, "a") as file:
									for i in passwords:
										file.write(f"\n\n{i}")
								passwords.insert(0, backup)
								print("The File has Successfully Created\n")
								key0 = True
								break
							elif len(passwords) == 1:
								with open(name, "w") as file:
									file.write(passwords[0])
								print("The File has Successfully Created\n")
								key0 = True
								break
						if key0:
							break
					else:
						print("Please enter a valid option\n")
					if key0:
						break
		elif returns == "both" or returns == "b" or returns.startswith("b"):
			while True:
				write = input("Do you want to put the file in the current Poject(P) folder or in another Location(L)?\n").lower()
				if write == "project" or write == "p" or write.startswith("p"):
					name = input("Write the name of the file\n")
					if " " in name[0] or " " in name[-1] or "\\" in name or "/" in name:
						print("Please don't put any space at the beginning and end of the name, and don't put any \"\\\" or \"/\" in the name\n")
						continue
					elif exists(name) and isdir(name):
						print("A directory already exist with that name\n")
						continue
					elif exists(name):
						while True:
							overwrite = input("A file already exist with that name but do you want to Overwrite(O) it or Append(A) over it? [Tip: If you don't want to Overwrite or Append over it then just press enter]\n").lower()
							if overwrite == "overwrite" or overwrite == "o" or overwrite.startswith("o"):
								if len(passwords) > 1:
									backup = passwords[0]
									with open(name, "w") as file:
										file.write(passwords[0])
										passwords.pop(0)
									with open(name, "a") as file:
										for i in passwords:
											file.write(f"\n\n{i}")
									passwords.insert(0, backup)
									print("The File has Successfully Overwritten\n")
									key0 = True
									break
								elif len(passwords) == 1:
									with open(name, "w") as file:
										file.write(passwords[0])
									print("The File has Successfully Overwritten\n")
									key0 = True
									break
							elif overwrite == "append" or overwrite == "a" or overwrite.startswith("a"):
								if len(passwords) > 1:
									with open(name, "a") as file:
										for i in passwords:
											file.write(f"\n\n{i}")
									print("The File has Successfully Appended\n")
									key0 = True
									break
								elif len(passwords) == 1:
									with open(name, "a") as file:
										file.write("\n\n"+passwords[0])
									print("The File has Successfully Appended\n")
									key0 = True
									break
							elif overwrite == "":
								break
							else:
								print("Please enter a valid option or just press enter if you don't want to Overwrite or append over it\n")
					else:
						if len(passwords) > 1:
							backup = passwords[0]
							with open(name, "w") as file:
								file.write(passwords[0])
								passwords.pop(0)
							with open(name, "a") as file:
								for i in passwords:
									file.write(f"\n\n{i}")
							passwords.insert(0, backup)
							print("The File has Successfully Created\n")
							key0 = True
							break
						elif len(passwords) == 1:
							with open(name, "w") as file:
								file.write(passwords[0])
							print("The File has Successfully Created\n")
							key0 = True
							break
					if key0:
						break
				elif write == "location" or write == "l" or write.startswith("l"):
					while True:
						location = input("Please enter the Location you want to put the file in (Please make use to add \ or / add the end according to your device)\n")
						if not exists(location) and not isdir(location):
							print("Please enter a valid Location\n")
							continue
						elif location[-1] != "/" and location[-1] != "\\":
							print('Please add "\\" or "/" at the end according to your device\n')
							continue
						else:
							break
					while True:
						name = input("Please enter the name of the file\n")
						if " " in name[0] or " " in name[-1] or "\\" in name or "/" in name:
							print("Please don't put any space at the beginning and end of the name, and don't put any \"\\\" or \"/\" in the name\n")
							continue
						name = location + name
						if exists(name) and isdir(name):
							print("A directory already exist with that name\n")
							continue
						elif exists(name):
							while True:
								overwrite = input("A file already exist with that name but do you want to Overwrite(O) it or Append(A) over it? [Tip: If you don't want to Overwrite or Append over it then just press enter]\n").lower()
								if overwrite == "overwrite" or overwrite == "o" or overwrite.startswith("o"):
									if len(passwords) > 1:
										backup = passwords[0]
										with open(name, "w") as file:
											file.write(passwords[0])
											passwords.pop(0)
										with open(name, "a") as file:
											for i in passwords:
												file.write(f"\n\n{i}")
										passwords.insert(0, backup)
										print("The File has Successfully Overwritten\n")
										key0 = True
										break
									elif len(passwords) == 1:
										with open(name, "w") as file:
											file.write(passwords[0])
										print("The File has Successfully Overwritten\n")
										key0 = True
										break
								elif overwrite == "append" or overwrite == "a" or overwrite.startswith("a"):
									if len(passwords) > 1:
										with open(name, "a") as file:
											for i in passwords:
												file.write(f"\n\n{i}")
										print("The File has Successfully Appended\n")
										key0 = True
										break
									elif len(passwords) == 1:
										with open(name, "a") as file:
											file.write("\n\n"+passwords[0])
										print("The File has Successfully Appended\n")
										key0 = True
										break
								elif overwrite == "":
									break
								else:
									print("Please enter a valid option or just press enter if you don't want to Overwrite or append over it\n")
						else:
							if len(passwords) > 1:
								backup = passwords[0]
								with open(name, "w") as file:
									file.write(passwords[0])
									passwords.pop(0)
								with open(name, "a") as file:
									for i in passwords:
										file.write(f"\n\n{i}")
								passwords.insert(0, backup)
								print("The File has Successfully Created\n")
								key0 = True
								break
							elif len(passwords) == 1:
								with open(name, "w") as file:
									file.write(passwords[0])
								print("The File has Successfully Created\n")
								key0 = True
								break
						if key0:
							break
				else:
					print("Please enter a valid option\n")
				if key0:
					break
			print("\nYour passwords are,\n\n")
			for i in passwords:
				print(f"{i}\n")
		elif returns == "":
			return passwords
		else:
			print("Please enter a valid option\n")
		if key0:
			break
passgen()