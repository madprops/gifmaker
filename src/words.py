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

	new_lines = []
	pattern = re.compile(r"\[(?P<word>random)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)

	for line in config.words:
		new_lines.append(re.sub(pattern, replace, line))

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