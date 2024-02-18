# Standard
import sys
import random
import string
import colorsys
from pathlib import Path

def random_string():
	vowels = "aeiou"
	consonants = "".join(set(string.ascii_lowercase) - set(vowels))

	def con():
		return random.choice(consonants)

	def vow():
		return random.choice(vowels)

	return con() + vow() + con() + vow() + con() + vow()

def get_extension(path):
	return Path(path).suffix.lower()

def resolve_path(path):
	pth = Path(path).expanduser()

	if pth.is_absolute():
		return full_path(pth)
	else:
		return full_path(Path(Path.cwd(), pth))

def full_path(path):
	return path.expanduser().resolve()

def exit(message):
	print(f"\nExit: {message}\n")
	sys.exit(1)

def read_toml(path):
	import tomllib

	if (not path.exists()) or (not path.is_file()):
		exit("TOML file does not exist")

	try:
		return tomllib.load(open(path, "rb"))
	except Exception as e:
		print(f"Error: {e}")
		exit("Failed to read TOML file")

def random_color(lightness):
	hue = random.random()
	saturation = 0.8
	r, g, b = colorsys.hsv_to_rgb(hue, saturation, lightness)
	r, g, b = int(r * 255), int(g * 255), int(b * 255)
	return r, g, b

def random_light():
	return random_color(0.8)

def random_dark():
	return random_color(0.2)