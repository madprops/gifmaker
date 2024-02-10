# Standard
from pathlib import Path

class Global:
	# Frames per second to use
	fps = 2.0

	# Number of frames to use if no words are provided
	frames = 3

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
	format = "gif"

	# The order to use when extracting the frames
	order = "random"

	# The font to use for the text. Either simple, complex, plain, duplex, or triplex
	font = "simple"

	# The size of the text
	fontsize = 3.0

	# The color of the text
	fontcolor = (255, 255, 255)

	# The thickness of the text
	boldness = 3

	repeat = "[again]"
	random_lower = "[random]"
	random_upper = "[RANDOM]"
	random_title = "[Random]"

def fill_paths(main):
	Global.root = main.parent.resolve()
	Global.input = Path(Global.root, "media", "video.webm").resolve()
	Global.output = Path(Global.root, "output").resolve()
	Global.wordfile = Path(Global.root, "data", "nouns.txt").resolve()