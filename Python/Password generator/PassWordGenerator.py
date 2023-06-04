from random import choice, shuffle
_num = ["0","1","2","3","4","5","6","7","8","9"]
_up = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
_low = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
_symb = ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","+","=","{","[","}","]","|","\\",":",";","\"","'","<",",",">",".","?","/"]
class PassWordGenerator:
    def quick(self, lenth, number = True, upper = True, lower = True, symbols = True):
        password = ""
        total = []
        if number: total.extend(_num)
        if upper: total.extend(_up)
        if lower: total.extend(_low)
        if symbols: total.extend(_symb)
        for i in range(lenth):
            shuffle(total)
            password += choice(total)
        return password
    def generate(self, generate, lenth, number = True, upper = True, lower = True, symbols = True):
        passwords = []
        total = []
        if number: total.extend(_num)
        if upper: total.extend(_up)
        if lower: total.extend(_low)
        if symbols: total.extend(_symb)
        for i in range(generate):
            password = ""
            for j in range(lenth):
                shuffle(total)
                password += choice(total)
            passwords.append(password)
        return passwords.copy()
_inst = PassWordGenerator()
quick = _inst.quick
generate = _inst.generate