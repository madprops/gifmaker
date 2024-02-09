# Standard
import random
import string
from pathlib import Path

NOUNS = []
HERE = Path(__file__).parent

def random_words(num):
	global NOUNS

	if len(NOUNS) == 0:
		file = Path(HERE, "nouns.txt")

		with open(file, "r") as file:
			lines = file.readlines()
			NOUNS = [item.strip() for line in lines for item in line.split() if item.strip()]

	return random.sample(NOUNS, num)

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