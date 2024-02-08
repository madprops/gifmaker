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

	return (
		random.choice(consonants) +
		random.choice(vowels) +
		random.choice(consonants) +
		random.choice(vowels) +
		random.choice(consonants) +
		random.choice(vowels)
	)

def is_number(s):
	try:
		return int(s)
	except:
		return 0