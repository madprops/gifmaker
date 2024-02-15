# Modules
from settings import Settings
import words

# Standard
import re
import random

def check_random():
	if not Settings.words:
		return

	def replace(match):
		n = match["number"]
		number = int(n) if n is not None else 1
		rand = match["word"]
		randwords = []

		for _ in range(number):
			if rand == "random":
				randwords.append(words.random_word().lower())
			elif rand == "RANDOM":
				randwords.append(words.random_word().upper())
			elif rand == "Random":
				randwords.append(words.random_word().title())

		return " ".join(randwords)

	new_words = []

	for line in Settings.words:
		pattern = re.compile(r"\[(?P<word>random)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		new_words.append(re.sub(pattern, replace, line))

	Settings.words = new_words

def check_repeat():
	if not Settings.words:
		return

	new_words = []

	for word in Settings.words:
		pattern = re.compile(r"\[(?P<word>repeat)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		match = re.match(pattern, word)

		if match:
			n = match["number"]
			number = int(n) if n is not None else 1
			new_words.extend([new_words[-1]] * number)
		else:
			new_words.append(word)

	Settings.words = new_words

def random_word():
	if not Settings.wordlist:
		with open(Settings.wordfile, "r") as file:
			lines = file.readlines()
			Settings.wordlist = [line.strip() for line in lines]

	return random.choice(Settings.wordlist)