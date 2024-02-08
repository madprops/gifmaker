import random
import string

def random_words(num_words):
	dict_words = "/usr/share/dict/words"

	with open(dict_words, "r") as file:
		words = file.read().splitlines()
		return random.sample(words, num_words)

def random_string():
	vowels = "aeiou"
	consonants = "".join(set(string.ascii_lowercase) - set(vowels))

	def cons():
		return random.choice(consonants)

	def vow():
		return random.choice(vowels)

	return cons() + vow() + cons() + vow() + cons() + vow()

def is_number(s):
	try:
		return int(s)
	except:
		return 0

def split_words(words, sep):
	return [s.strip() for s in words.split(sep) if s.strip()]