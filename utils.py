# Libraries
import nltk

# Standard
import random
import string

# Download the word list
# This should happen only once
nltk.download("words")
from nltk.corpus import words as WordList

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