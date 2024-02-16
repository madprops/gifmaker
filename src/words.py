# Modules
from configuration import config
import words

# Standard
import re
import random

def check_random():
	if not config.words:
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

	for line in config.words:
		pattern = re.compile(r"\[(?P<word>random)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		new_words.append(re.sub(pattern, replace, line))

	config.words = new_words

def check_repeat():
	if not config.words:
		return

	new_words = []

	for word in config.words:
		pattern = re.compile(r"\[(?P<word>repeat)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		match = re.match(pattern, word)

		if match:
			n = match["number"]
			number = int(n) if n is not None else 1
			new_words.extend([new_words[-1]] * number)
		else:
			new_words.append(word)

	config.words = new_words

def random_word():
	if not config.randomlist:
		with open(config.randomfile, "r") as file:
			lines = file.readlines()
			config.randomlist = [line.strip() for line in lines]

	return random.choice(config.randomlist)