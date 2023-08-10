import json
from collections import Counter

def common(words):
	cWords = [Counter(set(word)) for word in words]
	cCounts = sum(cWords, Counter())
	return sorted(words, key=lambda w: sum(cCounts[i] for i in set(w)))

with open("Word_lengths.json", "r") as file:
	Words = json.loads(file.read())

green = space = "-"
blacks = []
lenth = int(input("Enter the lenth of the word:\n"))
words = Words[str(lenth)]

while space in green:
	green = input("Enter the green letter:\n").strip().lower()
	nSGreen = green.replace(space, "")
	if nSGreen != "":
		fWords = [word for word in words if all(green[i] == space or green[i] == word[i] for i in range(len(green)))]
	else:
		green = space * lenth
		fWords = words.copy()
	
	yellow = input("Enter the yellow letter:\n").strip().lower()
	nSYellow = yellow.replace(space, "")
	if nSYellow != "":
		tWords = fWords.copy()
		fWords.clear()
		
		for word in tWords:
			lWord = list(word)
			key0 = True
			for i in nSGreen:
				lWord.remove(i)
			for i in nSYellow:
				if i in lWord:
					lWord.remove(i)
				else:
					key0 = False
					break
			if not key0:
				continue
			
			for i in range(len(yellow)):
				if green[i] == word[i]:
					continue
				if yellow[i] == word[i]:
					key0 = False
					break
			
			if key0:
				fWords.append(word)
	
	black = list(input("Enter the black letter:\n").strip().lower())
	blacks.extend(black)
	if len(blacks) != 0:
		fWords = [word for word in fWords if all(False if i in word else True for i in blacks)]
	
	fWords = common(fWords)
	print(fWords, end = "\n\n")