import json
from collections import Counter

def most_common_letter_word(words_list):
	
	word_counts = [Counter(set(word)) for word in words_list]
	#print(word_counts, end ="\n\n")
	combined_counts = sum(word_counts, Counter())
	print(combined_counts, end="\n\n")
	
	sorted_words = sorted(words_list, key=lambda w: sum(combined_counts[letter] for letter in set(w)), reverse=True)
	return sorted_words

with open("Word_lengths.json", "r") as F:
    Words = json.loads(F.read())

symbol = "-"
end = []
lenth = int(input("Enter the lenth of the pattern:\n"))
words = Words[str(lenth)]
pattern = symbol
while symbol in pattern:
	pattern = input("Enter the green letter:\n")
	letters = list(input("Enter the yellow letter:\n"))
	_end = list(input("Enter the black letter:\n"))
	
	for i in _end:
		end.append(i)
	
	result = []
	for word in words:
		if all(pattern[i] == symbol or word[i] == pattern[i] for i in range(len(pattern))):
			result.append(word)
	z = result.copy()
	result.clear()
	
	for r in z:
		a = list(r)
		b = True
		for i in range(len(pattern)):
			if pattern[i] != symbol:
				a.remove(pattern[i])
		for i in letters:
			if i in a:
				a.remove(i)
			else:
				b = False
				break
		if b:
			result.append(r)
	
	result = [word for word in result if all(False if i in word else True for i in end)]
	
	result = most_common_letter_word(result)
	
	result.reverse()
	
	print(result, end = "\n\n")