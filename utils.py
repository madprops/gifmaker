# Libraries
from english_words import get_english_words_set

# Standard
import random
import string

def random_words(num):
	words = list(get_english_words_set(['web2']))
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