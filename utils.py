# Libraries
from nltk.corpus import words as WordList

# Standard
import random
import string

def random_words(num):
	words = WordList.words()
	return random.sample(words, num)

def random_string():
	vowels = "aeiou"
	consonants = "".join(set(string.ascii_lowercase) - set(vowels))

	def con():
		return random.choice(consonants)

	def vow():
		return random.choice(vowels)

	return con() + vow() + con() + vow() + con() + vow()

def is_number(s):
	try:
		return int(s)
	except:
		return 0

def split_words(words, sep):
	return [s.strip() for s in words.split(sep) if s.strip()]