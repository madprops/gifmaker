# Modules
from modules.state import Global

# Standard
import random
import string
from pathlib import Path

def random_words(num):
	if len(Global.nouns) == 0:
		file = Path(Global.here, "nouns.txt")

		with open(file, "r") as file:
			lines = file.readlines()
			Global.nouns = [item.strip() for line in lines for item in line.split() if item.strip()]

	return random.sample(Global.nouns, num)

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