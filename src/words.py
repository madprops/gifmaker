# Modules
from args import Global
import words

# Standard
import re
import random

def check_random():
	if len(Global.words) == 0:
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

	for line in Global.words:
		pattern = re.compile(r"\[(?P<word>random)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		new_words.append(re.sub(pattern, replace, line))

	Global.words = new_words

def check_repeat():
	if len(Global.words) == 0:
		return

	new_words = []
	prev_word = None

	for word in Global.words:
		pattern = re.compile(r"\[(?P<word>repeat)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		match = re.match(pattern, word)

		if match:
			n = match["number"]
			number = int(n) if n is not None else 1
			new_words.extend([new_words[-1]] * number)
		else:
			new_words.append(word)

	Global.words = new_words

def random_word():
	if len(Global.wordlist) == 0:
		with open(Global.wordfile, "r") as file:
			lines = file.readlines()
			Global.wordlist = [line.strip() for line in lines]

	return random.choice(Global.wordlist)