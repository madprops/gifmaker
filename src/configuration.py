# Modules
import utils

# Standard
import argparse
from pathlib import Path
from typing import List, Union, Any
from argparse import Namespace

class Configuration:
	# Delay between frames
	delay = 600

	# Number of frames to use if no words are provided
	frames: Union[int, None] = None

	# The padding of the text from the left
	left: Union[int, None] = None

	# The padding of the text from the right
	right: Union[int, None] = None

	# The padding of the text from the top
	top: Union[int, None] = None

	# The padding of the text from the bottom
	bottom: Union[int, None] = None

	# The width to resize the frames
	width: Union[int, None] = None

	# Default words to use
	words: List[str] = []

	# File to use as the source of word lines
	wordfile: Union[Path, None] = None

	# The pool for random words
	randomlist: List[str] = []

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
	fontcolor: Union[List[int], str] = [255, 255, 255]

	# The thickness of the text
	boldness = 3

	# The color of the background
	bgcolor: Union[List[int], str, None] = None

	# The opacity of the background
	opacity = 0.5

	# The padding of the background
	padding = 25

	# Don't add the baseline to the background's height
	baseline = False

	# Path to a TOML file that defines the arguments to use
	script: Union[Path, None] = None

	# How to loop a gif render
	loop = 0

	# Spacing between lines
	linespace = 20

	# Linebreak character
	linebreak = "\\n"

	# Re-render the frames to change the width or delay
	remake = False

	# List of filters to use per frame
	filterlist: List[str] = []

	# The list of allowed filters when picking randomly
	filteropts: List[str] = []

	# Color filter to apply to frames
	filter = "none"

	# The list of frame indices to use
	framelist: List[str] = []

	# If this is False it will try to not repeat random words
	repeatrandom = False

	# If this is False it will try to not repeat random filters
	repeatfilter = False

	# Fill the rest of the frames with the last word line
	fillwords = False

	# --- INTERAL VARS

	# List to keep track of used random words
	randwords: List[str] = []

	def fill_paths(self, main_file: Path) -> None:
		self.root = utils.full_path(main_file.parent.parent)
		self.input = [utils.full_path(Path(self.root, "media", "video.webm"))]
		self.output = utils.full_path(Path(self.root, "output"))
		self.randomfile = utils.full_path(Path(self.root, "data", "nouns.txt"))

	def parse_args(self) -> None:
		p = argparse.ArgumentParser(description="Borat the Gif Maker")

		p.add_argument("--input", "-i", type=str, help="Path to the a video or image file. Separated by commas")
		p.add_argument("--words", type=str, help="Lines of words to use on the frames")
		p.add_argument("--wordfile", type=str, help="Path of file with word lines")
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
		p.add_argument("--randomlist", type=str, help="List of words to consider for random words")
		p.add_argument("--randomfile", type=str, help="Path to a list of words to consider for random words")
		p.add_argument("--script", type=str, help="Path to a TOML file that defines the arguments to use")
		p.add_argument("--loop", type=int, help="How to loop a gif render")
		p.add_argument("--linespace", type=int, help="Spacing between lines")
		p.add_argument("--linebreak", type=str, help="Linebreak character")
		p.add_argument("--remake", action="store_true", help="Re-render the frames to change the width or delay")
		p.add_argument("--filter", type=str, choices=[
			"hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8", "anyhue", "anyhue2",
			"gray", "blur", "invert", "saturate", "random", "random2", "none",
			], help="Color filter to apply to frames")
		p.add_argument("--filterlist", type=str, help="Filters to use per frame. Separated by commas")
		p.add_argument("--filteropts", type=str, help="The list of allowed filters when picking randomly. Separated by commas")
		p.add_argument("--framelist", type=str, help="List of frame indices to use. Separated by commas")
		p.add_argument("--repeatrandom", action="store_true", help="Repeating random words is ok")
		p.add_argument("--repeatfilter", action="store_true", help="Repeating random filters is ok")
		p.add_argument("--fillwords", action="store_true", help="Fill the rest of the frames with the last word line")

		args = p.parse_args()

		def get_list(value: str, vtype: Any, separator: str) -> List[Any]:
			return list(map(vtype, map(str.strip, value.split(separator))))

		def normal(attr: str) -> None:
			value = getattr(args, attr)

			if value is not None:
				setattr(self, attr, value)

		def commas(attr: str, vtype: Any) -> None:
			value = getattr(args, attr)

			if value is not None:
				if not "," in value:
					setattr(self, attr, value)
				else:
					setattr(self, attr, get_list(value, vtype, ","))

		def path(attr: str) -> None:
			value = getattr(args, attr)

			if value is not None:
				setattr(self, attr, utils.resolve_path(value))

		def pathlist(attr: str) -> None:
			value = getattr(args, attr)

			if value is not None:
				paths = [utils.resolve_path(p.strip()) for p in value.split(",")]
				setattr(self, attr, paths)

		# Get script args first
		path("script")
		self.check_script(args)

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
		normal("separator")
		normal("linespace")
		normal("linebreak")
		normal("filter")
		normal("remake")
		normal("repeatrandom")
		normal("repeatfilter")
		normal("fillwords")

		commas("fontcolor", int)
		commas("bgcolor", int)
		commas("filterlist", str)
		commas("filteropts", str)
		commas("framelist", int)

		pathlist("input")
		path("output")
		path("wordfile")
		path("randomfile")

		self.check_args(args)

	def check_args(self, args: Namespace) -> None:
		def separate(value: str) -> List[str]:
			return [item.strip() for item in value.split(self.separator)]

		for path in self.input:
			if not path.exists() or not path.is_file():
				utils.exit("Input file does not exist")
				return None

		if self.wordfile:
			if not self.wordfile.exists() or not self.wordfile.is_file():
				utils.exit("Word file does not exist")
				return None

			self.read_wordfile()
		elif args.words:
			self.words = separate(args.words)

		if args.randomlist:
			self.randomlist = separate(args.randomlist)

		if not self.randomfile.exists() or not self.randomfile.is_file():
			utils.exit("Word file does not exist")
			return None

		self.set_color("fontcolor")
		self.set_color("bgcolor")

	def set_color(self, attr: str) -> None:
		value = getattr(self, attr)

		if value == "light":
			setattr(self, attr, utils.random_light())
		elif value == "dark":
			setattr(self, attr, utils.random_dark())

	def check_script(self, args: Namespace) -> None:
		if self.script is None:
			return

		data = utils.read_toml(Path(self.script))

		if data:
			for key in data:
				k = key.replace("-", "_")
				setattr(args, k, data[key])

	def read_wordfile(self) -> None:
		if config.wordfile:
			self.words = config.wordfile.read_text().splitlines()

# Main configuration object
config = Configuration()