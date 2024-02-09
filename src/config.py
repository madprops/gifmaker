# Standard
from pathlib import Path

class Global:
	# Frames per second to use
	fps = 2.11

	# Number of frames to use if no words are provided
	frames = 3

	# The size of the text
	size = 3

	# The thickness of the text
	thick = 3

	# The padding from the left
	left = None

	# The padding from the right
	right = None

	# The padding from the top
	top = None

	# The padding from the bottom
	bottom = None

	# The width to resize the frames
	width = None

	# Default words to use
	words = []

	# The list of nouns to use
	wordlist = []

	# The separator to use when splitting word lines
	separator = ";"

	# The format of the output file. Either gif or mp4
	ext = "gif"

	# The order to use when extracting the frames
	order = "random"

def fill_paths(main):
	Global.root = main.parent.resolve()
	Global.input = Path(Global.root, "media", "video.webm").resolve()
	Global.output = Path(Global.root, "output").resolve()
	Global.wordfile = Path(Global.root, "data", "nouns.txt").resolve()