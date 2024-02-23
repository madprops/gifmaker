# Modules
from configuration import config
import utils

# Standard
import re
import random
from typing import List, Any

def replace_random() -> None:
	if not config.words:
		return

	def replace(match: re.Match[Any]) -> str:
		word = match["word"].lower()
		num1 = None
		num2 = None

		if match["number1"]:
			num1 = int(match["number1"])

		if match["number2"]:
			num2 = int(match["number2"])

		if word == "number":
			if num1 is not None and num2 is not None:
				return str(random.randint(num1, num2))

		randwords: List[str] = []

		if (num1 is None) or (num1 < 1):
			num1 = 1

		for _ in range(num1):
			allow_zero = True

			if num1 > 1:
				if len(randwords) == 0:
					allow_zero = False

			randwords.append(get_random(match["word"], allow_zero))

		if word == "number":
			return "".join(randwords)
		else:
			return " ".join(randwords)

	new_lines: List[str] = []
	pattern = re.compile(r"\[(?P<word>randomx?|number)(?:\s+(?P<number1>\d+)(?:\s*(.+?)\s*(?P<number2>\d+))?)?\]", re.IGNORECASE)
	pattern_multi = re.compile(r"\[(?:x(?P<number>\d+))?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.search(pattern, line)

		if match:
			multi = 1
			match_multi = re.search(pattern_multi, line)

			if match_multi:
				multi = max(1, int(match_multi["number"]))
				line = re.sub(pattern_multi, "", line).strip()

			for _ in range(multi):
				new_line = re.sub(pattern, replace, line)
				new_lines.append(new_line)
		else:
			new_lines.append(line)

	config.words = new_lines

def replace_repeat() -> None:
	if not config.words:
		return

	new_lines: List[str] = []
	pattern = re.compile(r"^\[(?P<word>rep(?:eat)?)\s*(?P<number>\d+)?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.match(pattern, line)

		if match:
			num = match["number"]
			number = int(num) if num is not None else 1
			new_lines.extend([new_lines[-1]] * number)
		else:
			new_lines.append(line)

	config.words = new_lines

def replace_empty() -> None:
	if not config.words:
		return

	new_lines: List[str] = []
	pattern = re.compile(r"^\[(?P<word>empty)(?:\s+(?P<number>\d+))?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.match(pattern, line)

		if match:
			num = match["number"]
			number = int(num) if num is not None else 1

			for _ in range(number):
				new_lines.append("")
		else:
			new_lines.append(line)

	config.words = new_lines

def replace_date() -> None:
	if not config.words:
		return

	def replace(match: re.Match[Any]) -> str:
		fmt = match["format"] or "%H:%M:%S"
		return utils.get_date(fmt)

	new_lines: List[str] = []
	pattern = re.compile(r"\[(?P<word>date)(?:\s+(?P<format>.*))?\]", re.IGNORECASE)

	for line in config.words:
		match = re.search(pattern, line)

		if match:
			new_lines.append(re.sub(pattern, replace, line))
		else:
			new_lines.append(line)

	config.words = new_lines

def replace_count() -> None:
	if not config.words:
		return

	def replace(match: re.Match[Any]) -> str:
		config.wordcount += 1
		return str(config.wordcount)

	new_lines: List[str] = []
	pattern = re.compile(r"\[(?P<word>count)\]", re.IGNORECASE)

	for line in config.words:
		match = re.search(pattern, line)

		if match:
			new_lines.append(re.sub(pattern, replace, line))
		else:
			new_lines.append(line)

	config.words = new_lines

def random_word() -> str:
	if not config.randomlist:
		lines = config.randomfile.read_text().splitlines()
		config.randomlist = [line.strip() for line in lines]

	if not config.randwords:
		config.randwords = config.randomlist.copy()

	if not config.randwords:
		return ""

	w = random.choice(config.randwords)

	if not config.repeatrandom:
		config.randwords.remove(w)

	return w

def get_random(rand: str, allow_zero: bool) -> str:
	if rand == "random":
		return random_word().lower()
	elif rand == "RANDOM":
		return random_word().upper()
	elif rand == "Random":
		return random_word().capitalize()
	elif rand == "RanDom":
		return random_word().title()
	elif rand == "randomx":
		return random_word()
	elif rand == "number":
		return str(utils.random_digit(allow_zero))
	else:
		return ""