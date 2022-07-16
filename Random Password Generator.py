def passgen():
	from random import choice, shuffle
	a = ["0","1","2","3","4","5","6","7","8","9"]
	b = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	c = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	d = ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","+","=","{","[","}","]","|","\\",":",";","\"","'","<",",",">",".","?","/"]
	passwords = []
	generate = ""
	def normal():
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
		A = []
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
			remove = ""
			while True:
				try:
					print("[Normal] What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any space between them)\n")
					A.sort()
					for i in A:
						print(i,end=" ")
					remove = input("\n\n")
					for i in remove:
						A.remove(i)
						recovery += i
					break
				except ValueError:
					if not recovery == "":
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
		return passwords
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
				remove = ""
				while True:
					try:
						print("[Full] What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any space between them)\n")
						A.sort()
						for i in A:
							print(i,end=" ")
						remove = input("\n\n")
						for i in remove:
							A.remove(i)
							recovery += i
						break
					except ValueError:
						if not recovery == "":
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
			return passwords
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
					remove = ""
					while True:
						try:
							print(f"[Full] {position} password: What do you want to exclude? [Tip: Just pressing enter will exclude nothing] (Write the symbols, numbers or letters you want to exclude and do NOT put any space between them)\n")
							A.sort()
							for i in A:
								print(i,end=" ")
							remove = input("\n\n")
							for i in remove:
								A.remove(i)
								recovery += i
							break
						except ValueError:
							if not recovery == "":
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
			return passwords
	while True:
		choose = input("Choose one\nMode: Normal(N), Full(F)\n").lower()
		if choose == "normal" or choose == "n" or choose.startswith("n"):
			passwords = normal()
			break
		elif choose == "full" or choose == "f" or choose.startswith("f"):
			passwords = full()
			break
		else:
			print("Please choose a valid Mode\n")
	return passwords
passwords = passgen()
print("\nYour passwords are,\n\n")
for i in passwords:
	print(f"{i}\n")
