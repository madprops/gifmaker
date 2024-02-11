# Modules
from config import Global
import words

# Standard
import random

def check_random():
	if len(Global.words) == 0:
		return

	num_random = 0

	for rs in [Global.random_lower, Global.random_upper, Global.random_title]:
		num_random += sum(w.count(rs) for w in Global.words)

	if num_random == 0:
		return

	for i, line in enumerate(Global.words):
		new_words = []

		for word in line.split():
			new_word = word

			if word == Global.random_lower:
				new_word = words.random_word().lower()
			elif word == Global.random_upper:
				new_word = words.random_word().upper()
			elif word == Global.random_title:
				new_word = words.random_word().title()

			new_words.append(new_word)

		Global.words[i] = " ".join(new_words)

def check_repeat():
	if len(Global.words) == 0:
		return

	for i, word in enumerate(Global.words):
		if i == 0:
			continue

		if word == Global.repeat:
			prev = Global.words[i - 1]
			Global.words[i] = prev

def random_word():
	if len(Global.wordlist) == 0:
		with open(Global.wordfile, "r") as file:
			lines = file.readlines()
			Global.wordlist = [item.strip() for line in lines for item in line.split() if item.strip()]

	return random.choice(Global.wordlist)