def passgen():
    from random import choice, shuffle
    passwords = []
    a = ["0","1","2","2","3","4","5","6","7","8","9"]
    b = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    c = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    d = ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","+","=","{","[","}","]","|","\\",":",";","\"","'","<",",",">",".","?","/"]
    generate = ""
    while True:
        try:
            generate = input("How many passwords do you want to generate? (Just pressing Enter will generate one password)\n")
            generate = int(generate)
            if generate <= 0:
                print("Please enter only numbers that are larger than 0 or just press Enter to generate one password\n")
            else:
                break
        except ValueError:
            if generate == "":
                generate = 1
                break
            else:
                print("Please enter only numbers or just press Enter to generate one password\n")
    A = []
    while True:
            try:
                lenth = int(input("How many characters do you want in your password?\n"))
                if lenth <= 0:
                    print("Please enter only numbers that are larger than 0\n")
                else:
                    break
            except ValueError:
                print("Please enter only numbers\n")
    number = input("Do you want any numbers in your password? Y/N\n").lower()
    uppercase = input("Do you want any uppercase letters in your password? Y/N\n").lower()
    lowercase = input("Do you want any lowercase letters in your password? Y/N\n").lower()
    special = input("Do you want any special characters in your password? Y/N\n").lower()
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
    for i in range(generate):
        #A = []
        """
        while True:
            try:
                lenth = int(input("How many characters do you want in your password?\n"))
                if lenth <= 0:
                    print("Please enter only numbers that are larger than 0\n")
                else:
                    break
            except ValueError:
                print("Please enter only numbers\n")
        """
        #number = input("Do you want any numbers in your password? Y/N\n").lower()
        #if number == "yes" or number == "y" or number.startswith("y"):
	    #    for i in a:
		#        A.append(i)
        #uppercase = input("Do you want any uppercase letters in your password? Y/N\n").lower()
        #if uppercase == "yes" or uppercase == "y" or uppercase.startswith("y"):
	    #    for i in c:
		#        A.append(i)
        #lowercase = input("Do you want any lowercase letters in your password? Y/N\n").lower()
        #if lowercase == "yes" or lowercase == "y" or lowercase.startswith("y"):
	    #    for i in b:
		#        A.append(i)
        #special = input("Do you want any special characters in your password? Y/N\n").lower()
        #if special == "yes" or special == "y" or special.startswith("y"):
	    #    for i in d:
		#        A.append(i)
        password = ""
        for i in range(lenth):
	        shuffle(A)
	        B = choice(A)
	        password = password + B
        passwords.append(password)
    return passwords
passwords = passgen()
print("Your passwords are,\n\n")
for i in passwords:
    print(f"{i}\n")
