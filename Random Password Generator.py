import random
A = []
a = ["0","1","2","2","3","4","5","6","7","8","9"]
b = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
c = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
d = ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","+","=","{","[","}","]","|","\\",":",";","\"","'","<",",",">",".","?","/"]
password = ""
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
if number == "yes" or number == "y" or number.startswith("y"):
	for i in a:
		A.append(i)
uppercase = input("Do you want any uppercase letters in your password? Y/N\n").lower()
if uppercase == "yes" or uppercase == "y" or uppercase.startswith("y"):
	for i in c:
		A.append(i)
lowercase = input("Do you want any lowercase letters in your password? Y/N\n").lower()
if lowercase == "yes" or lowercase == "y" or lowercase.startswith("y"):
	for i in b:
		A.append(i)
special = input("Do you want any special characters in your password? Y/N\n").lower()
if special == "yes" or special == "y" or special.startswith("y"):
	for i in d:
		A.append(i)
for i in range(lenth):
	random.shuffle(A)
	b = random.choice(A)
	password = password + b
print(f"Your password is,    {password}")
