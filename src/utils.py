# Modules
from config import Global

# Standard
import random
import string
from pathlib import Path

def random_words(num):
	if len(Global.wordlist) == 0:
		with open(Global.wordfile, "r") as file:
			lines = file.readlines()
			Global.wordlist = [item.strip() for line in lines for item in line.split() if item.strip()]

	return random.sample(Global.wordlist, num)

def random_string():
	vowels = "aeiou"
	consonants = "".join(set(string.ascii_lowercase) - set(vowels))

	def con():
		return random.choice(consonants)

	def vow():
		return random.choice(vowels)

	return con() + vow() + con() + vow() + con() + vow()

def get_ext(path):
	return Path(path).suffix.lower()

def resolve_path(path):
	pth = Path(path)

	if pth.is_absolute():
		return pth
	else:
		return (Path.cwd() / pth).resolve()

def is_number(s):
	try:
		return int(s)
	except:
		return 0