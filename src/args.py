# Modules
import utils

# Standard
import argparse
from pathlib import Path

class Global:
	# Frames per second to use
	delay = 500

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

	# The pool for random words
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
	fontsize = 2.6

	# The color of the text
	fontcolor = (255, 255, 255)

	# The thickness of the text
	boldness = 3

	# The color of the background
	bgcolor = None

	# The opacity of the background
	opacity = 0.5

	# The padding of the background
	padding = 10

	# Don't add the baseline to the background's height
	no_baseline = False

	# Path to a TOML file that defines the arguments to use
	script = None

	# How to loop a gif render
	loop = 0

	# Spacing between lines
	linespace = 20

	# Linebreak character
	linebreak = "\\n"

	# Color filter to apply to frames
	filter = None

def parse_args():
	p = argparse.ArgumentParser(description="Borat the Gif Maker")

	p.add_argument("--input", "-i", type=str, help="Path to the a video or image file")
	p.add_argument("--words", type=str, help="Lines of words to use on the frames")
	p.add_argument("--delay", type=int, help="The delay in ms between frames")
	p.add_argument("--left", type=int, help="Left padding")
	p.add_argument("--right", type=int, help="Right padding")
	p.add_argument("--top", type=int, help="Top padding")
	p.add_argument("--bottom", type=int, help="Bottom padding")
	p.add_argument("--width", type=int, help="Width to resize the frames")
	p.add_argument("--frames", type=int, help="Number of frames to use if no words are provided")
	p.add_argument("--output", "-o", type=str, help="Output directory to save the file")
	p.add_argument("--format", type=str, choices=["gif", "mp4"], help="The format of the output file")
	p.add_argument("--separator", type=str, help="Character to use as the separator")
	p.add_argument("--order", type=str, choices=["random", "normal"], help="The order to use when extracting the frames")
	p.add_argument("--font", type=str, choices=["simple", "complex", "plain", "duplex", "triplex"], help="The font to use for the text")
	p.add_argument("--fontsize", type=float, help="Text size")
	p.add_argument("--fontcolor", type=str, help="Text color. 3 numbers from 0 to 255, separated by commas")
	p.add_argument("--boldness", type=int, help="Text thickness")
	p.add_argument("--bgcolor", type=str, help="Add a background rectangle for the text with this color. 3 numbers from 0 to 255, separated by commas")
	p.add_argument("--opacity", type=float, help="The opacity of the background rectangle")
	p.add_argument("--padding", type=int, help="The padding of the background rectangle")
	p.add_argument("--no-baseline", action="store_true", help="Don't add the baseline to the background rectangle's height")
	p.add_argument("--wordlist", type=str, help="List of words to consider for random words. Separated by commas")
	p.add_argument("--script", type=str, help="Path to a TOML file that defines the arguments to use")
	p.add_argument("--loop", type=int, help="How to loop a gif render")
	p.add_argument("--linespace", type=int, help="Spacing between lines")
	p.add_argument("--linebreak", type=str, help="Linebreak character")
	p.add_argument("--filter", type=str, choices=[
		"hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8",
		"invert", "saturation", "sepia", "grayscale", "blur",
		], help="Color filter to apply to frames")

	args = p.parse_args()

	def proc(attr):
		value = getattr(args, attr)

		if value is not None:
			setattr(Global, attr, value)

	def commas(attr, vtype):
		value = getattr(args, attr)

		if value is not None:
			setattr(Global, attr, tuple(map(vtype, value.split(","))))

	def path(attr):
		value = getattr(args, attr)

		if value is not None:
			setattr(Global, attr, utils.resolve_path(value))

	# Get script args first
	path("script")
	check_script(args)

	# Needed for 'words'
	proc("separator")

	if args.words is not None:
		Global.words = [word.strip() for word in args.words.split(Global.separator)]

	path("input")
	path("output")

	proc("delay")
	proc("fontsize")
	proc("boldness")
	proc("opacity")
	proc("left")
	proc("right")
	proc("top")
	proc("bottom")
	proc("width")
	proc("format")
	proc("order")
	proc("font")
	proc("frames")
	proc("padding")
	proc("no_baseline")
	proc("loop")
	proc("linespace")
	proc("linebreak")
	proc("filter")

	commas("fontcolor", int)
	commas("bgcolor", int)
	commas("wordlist", str)

	if not Global.input.exists() or \
	not Global.input.is_file():
		utils.exit("Input file does not exist")

def fill_paths(main_file):
	Global.root = utils.full_path(Path(main_file).parent.parent)
	Global.input = utils.full_path(Path(Global.root, "media", "video.webm"))
	Global.output = utils.full_path(Path(Global.root, "output"))
	Global.wordfile = utils.full_path(Path(Global.root, "data", "nouns.txt"))

def check_script(args):
	if Global.script is None:
		return

	data = utils.read_toml(Path(Global.script))

	for key in data:
		k = key.replace("-", "_")
		setattr(args, k, data[key])