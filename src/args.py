# Modules
import utils

# Standard
import argparse
from pathlib import Path

class Global:
	# Frames per second to use
	delay = 500

	# Number of frames to use if no words are provided
	frames = None

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
	fontsize = 2.5

	# The color of the text
	fontcolor = (255, 255, 255)

	# The thickness of the text
	boldness = 3

	# The color of the background
	bgcolor = None

	# The opacity of the background
	opacity = 0.5

	# The padding of the background
	padding = 33

	# Don't add the baseline to the background's height
	baseline = False

	# Path to a TOML file that defines the arguments to use
	script = None

	# How to loop a gif render
	loop = 0

	# Spacing between lines
	linespace = 20

	# Linebreak character
	linebreak = "\\n"

	# Re-render the frames to change the width or delay
	remake = False

	# List of filters to use per frame
	filterlist = []

	# Color filter to apply to frames
	filter = None

	# The list of frame indices to use in order
	framelist = []

def parse_args():
	p = argparse.ArgumentParser(description="Borat the Gif Maker")

	p.add_argument("--input", "-i", type=str, help="Path to the a video or image file. Separated by semicolons")
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
	p.add_argument("--baseline", action="store_true", help="Add the baseline to the background rectangle's height")
	p.add_argument("--wordlist", type=str, help="List of words to consider for random words. Separated by semicolons")
	p.add_argument("--wordfile", type=str, help="Path to a list of words to consider for random words")
	p.add_argument("--script", type=str, help="Path to a TOML file that defines the arguments to use")
	p.add_argument("--loop", type=int, help="How to loop a gif render")
	p.add_argument("--linespace", type=int, help="Spacing between lines")
	p.add_argument("--linebreak", type=str, help="Linebreak character")
	p.add_argument("--remake", action="store_true", help="Re-render the frames to change the width or delay")
	p.add_argument("--filter", type=str, choices=[
		"hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8",
		"gray", "blur", "invert", "saturate", "random", "random2"
		], help="Color filter to apply to frames")
	p.add_argument("--filterlist", type=str, help="Filters to use per frame. Separated by semicolons")
	p.add_argument("--framelist", type=str, help="List of frame indices to use. Separated by semicolons")

	args = p.parse_args()

	def get_list(value, vtype, separator):
		return list(map(vtype, map(str.strip, value.split(separator))))

	def normal(attr):
		value = getattr(args, attr)

		if value is not None:
			setattr(Global, attr, value)

	def commas(attr, vtype):
		value = getattr(args, attr)

		if value is not None:
			setattr(Global, attr, get_list(value, vtype, ","))

	def semicolons(attr, vtype):
		value = getattr(args, attr)

		if value is not None:
			setattr(Global, attr, get_list(value, vtype, ";"))

	def path(attr):
		value = getattr(args, attr)

		if value is not None:
			setattr(Global, attr, utils.resolve_path(value))

	def pathlist(attr):
		value = getattr(args, attr)

		if value is not None:
			paths = [utils.resolve_path(p.strip()) for p in value.split(";")]
			setattr(Global, attr, paths)

	# Get script args first
	path("script")
	check_script(args)

	# Needed for 'words'
	normal("separator")

	if args.words is not None:
		Global.words = [word.strip() for word in args.words.split(Global.separator)]

	normal("delay")
	normal("fontsize")
	normal("boldness")
	normal("opacity")
	normal("left")
	normal("right")
	normal("top")
	normal("bottom")
	normal("width")
	normal("format")
	normal("order")
	normal("font")
	normal("frames")
	normal("padding")
	normal("baseline")
	normal("loop")
	normal("linespace")
	normal("linebreak")
	normal("filter")
	normal("remake")

	commas("fontcolor", int)
	commas("bgcolor", int)

	semicolons("wordlist", str)
	semicolons("filterlist", str)
	semicolons("framelist", int)

	pathlist("input")
	path("output")
	path("wordfile")

	for path in Global.input:
		if not path.exists() or not path.is_file():
			utils.exit("Input file does not exist")

	if not Global.wordfile.exists() or not Global.wordfile.is_file():
		utils.exit("Word file does not exist")

def fill_paths(main_file):
	Global.root = utils.full_path(Path(main_file).parent.parent)
	Global.input = [utils.full_path(Path(Global.root, "media", "video.webm"))]
	Global.output = utils.full_path(Path(Global.root, "output"))
	Global.wordfile = utils.full_path(Path(Global.root, "data", "nouns.txt"))

def check_script(args):
	if Global.script is None:
		return

	data = utils.read_toml(Path(Global.script))

	for key in data:
		k = key.replace("-", "_")
		setattr(args, k, data[key])