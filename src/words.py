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
			randwords.append(get_rand_word(rand))

		return " ".join(randwords)

	new_lines = []
	pattern = re.compile(r"\[(?P<word>random)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
	pattern_multi = re.compile(r"\[(?:x(?P<number>\d+))?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.search(pattern, line)

		if match:
			multi = 1
			match_multi = re.search(pattern_multi, line)

			if match_multi:
				multi = max(1, int(match_multi["number"]))
				line = re.sub(pattern_multi, "", line)

			for _ in range(multi):
				new_line = re.sub(pattern, replace, line)
				new_lines.append(new_line)
		else:
			new_lines.append(line)

	config.words = new_lines

def check_repeat():
	if not config.words:
		return

	new_lines = []
	pattern = re.compile(r"^\[(?P<word>repeat)(?:\s+(?P<number>\d+))?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.match(pattern, line)

		if match:
			n = match["number"]
			number = int(n) if n is not None else 1
			new_lines.extend([new_lines[-1]] * number)
		else:
			new_lines.append(line)

	config.words = new_lines

def check_empty():
	if not config.words:
		return

	new_lines = []
	pattern = re.compile(r"^\[(?P<word>empty)\]$", re.IGNORECASE)

	for line in config.words:
		match = re.match(pattern, line)

		if match:
			new_lines.append("")
		else:
			new_lines.append(line)

	config.words = new_lines

def random_word():
	if not config.randomlist:
		lines = config.randomfile.read_text().splitlines()
		config.randomlist = [line.strip() for line in lines]

	return random.choice(config.randomlist)

def get_rand_word(rand):
	if rand == "random":
		return words.random_word().lower()
	elif rand == "RANDOM":
		return words.random_word().upper()
	elif rand == "Random":
		return words.random_word().title()
	else:
		return ""