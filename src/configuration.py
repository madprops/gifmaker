# Modules
import utils

# Standard
import argparse
import codecs
import textwrap
from argparse import Namespace
from typing import List, Union, Any
from pathlib import Path

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

	# The height to resize the frames
	height: Union[int, None] = None

	# Default words to use
	words: List[str] = []

	# File to use as the source of word lines
	wordfile: Union[Path, None] = None

	# The pool for random words
	randomlist: List[str] = []

	# The separator to use when splitting word lines
	separator = ";"

	# The format of the output file. Either gif, webm, mp4, jpg, or png
	format = "gif"

	# The order to use when extracting the frames
	order = "random"

	# The font to use for the text. Either simple, complex, plain, duplex, or triplex
	font = "simple"

	# The size of the text
	fontsize = 50

	# The color of the text
	fontcolor: Union[List[int], str] = [255, 255, 255]

	# The color of the background
	bgcolor: Union[List[int], str, None] = None

	# The color of the outline
	outline: Union[List[int], str, None] = None

	# The width of the outline
	outlinewidth = 2

	# The opacity of the background
	opacity = 0.6

	# The padding of the background
	padding = 20

	# The border radius of the background
	radius = 0

	# How to align the text
	align = "center"

	# Path to a TOML file that defines the arguments to use
	script: Union[Path, None] = None

	# How to loop a gif render
	loop = 0

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

	# Don't resize if the frames are going to be bigger than the original
	nogrow = False

	# Split line if it exceeds this char length
	wrap = 30

	# --- INTERAL VARS

	# List to keep track of used random words
	randwords: List[str] = []

	# Counter for [count]
	wordcount = 0

	# Last font color used
	last_fontcolor = None

	def fill_paths(self, main_file: str) -> None:
		self.root = utils.full_path(Path(main_file).parent.parent)
		self.input = [utils.full_path(Path(self.root, "media", "video.webm"))]
		self.output = utils.full_path(Path(self.root, "output"))
		self.randomfile = utils.full_path(Path(self.root, "data", "nouns.txt"))
		self.fontspath = utils.full_path(Path(self.root, "fonts"))

	def parse_args(self) -> None:
		parser = argparse.ArgumentParser(description="Gif Maker")

		argdefs = [
			{"name": "input", "type": str, "help": "Path to the a video or image file. Separated by commas"},
			{"name": "words", "type": str, "help": "Lines of words to use on the frames"},
			{"name": "wordfile", "type": str, "help": "Path of file with word lines"},
			{"name": "delay", "help": "The delay in ms between frames"},
			{"name": "left", "type": int, "help": "Left padding"},
			{"name": "right", "type": int, "help": "Right padding"},
			{"name": "top", "type": int, "help": "Top padding"},
			{"name": "bottom", "type": int, "help": "Bottom padding"},
			{"name": "width", "type": int, "help": "Width to resize the frames"},
			{"name": "height", "type": int, "help": "Height to resize the frames"},
			{"name": "frames", "type": int, "help": "Number of frames to use if no words are provided"},
			{"name": "output", "type": str, "help": "Output directory to save the file"},
			{"name": "format", "type": str, "choices": ["gif", "webm", "mp4", "jpg", "png"], "help": "The format of the output file"},
			{"name": "separator", "type": str, "help": "Character to use as the separator"},
			{"name": "order", "type": str, "choices": ["random", "normal"], "help": "The order to use when extracting the frames"},
			{"name": "font", "type": str, "choices": ["sans", "serif", "mono", "bold", "italic"], "help": "The font to use for the text"},
			{"name": "fontsize", "help": "The size of the font"},
			{"name": "fontcolor", "type": str, "help": "Text color. 3 numbers from 0 to 255, separated by commas. Names like 'red' are also supported"},
			{"name": "bgcolor", "type": str, "help": "Add a background rectangle for the text with this color. 3 numbers from 0 to 255, separated by commas. Names like 'red' are also supported"},
			{"name": "outline", "type": str, "help": "Add an outline around the text with this color. 3 numbers from 0 to 255, separated by commas. Names like 'red' are also supported"},
			{"name": "outlinewidth", "type": str, "help": "The width of the outline"},
			{"name": "opacity", "help": "The opacity of the background rectangle"},
			{"name": "padding", "help": "The padding of the background rectangle"},
			{"name": "radius", "help": "The border radius of the background"},
			{"name": "align", "type": str, "choices": ["left", "center", "right"], "help": "How to align the center when there are multiple lines"},
			{"name": "randomlist", "type": str, "help": "List of words to consider for random words"},
			{"name": "randomfile", "type": str, "help": "Path to a list of words to consider for random words"},
			{"name": "script", "type": str, "help": "Path to a TOML file that defines the arguments to use"},
			{"name": "loop", "type": int, "help": "How to loop a gif render"},
			{"name": "remake", "action": "store_true", "help": "Re-render the frames to change the width or delay"},
			{"name": "filter", "type": str, "choices": [
				"hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8", "anyhue", "anyhue2",
				"gray", "blur", "invert", "random", "random2", "none",
				], "help": "Color filter to apply to frames"},
			{"name": "filterlist", "type": str, "help": "Filters to use per frame. Separated by commas"},
			{"name": "filteropts", "type": str, "help": "The list of allowed filters when picking randomly. Separated by commas"},
			{"name": "framelist", "type": str, "help": "List of frame indices to use. Separated by commas"},
			{"name": "repeatrandom", "action": "store_true", "help": "Repeating random words is ok"},
			{"name": "repeatfilter", "action": "store_true", "help": "Repeating random filters is ok"},
			{"name": "fillwords", "action": "store_true", "help": "Fill the rest of the frames with the last word line"},
			{"name": "nogrow", "action": "store_true", "help": "Don't resize if the frames are going to be bigger than the original"},
			{"name": "wrap", "type": str, "help": "Split line if it exceeds this char length"},
		]

		def prepare_parser():
			aliases = {
				"input": ["--i", "-i"],
				"output": ["--o", "-o"],
			}

			for item in argdefs:
				name = item["name"]
				names = [f"--{name}", f"-{name}"]

				if name in aliases:
					names += aliases[name]

				opts = ["type", "choices", "help", "action"]
				tail = {key: item[key] for key in opts if key in item}

				parser.add_argument(*names, **tail)

		# ---------

		prepare_parser()
		args = parser.parse_args()

		# ---------

		def get_list(attr: str, value: str, vtype: Any, separator: str) -> List[Any]:
			try:
				lst = list(map(vtype, map(str.strip, value.split(separator))))
			except:
				utils.exit(f"Failed to parse '--{attr}'")
				return []

			return lst

		def normal(attr: str) -> None:
			value = getattr(args, attr)

			if value is not None:
				setattr(self, attr, value)

		def commas(attr: str, vtype: Any) -> None:
			value = getattr(args, attr)

			if value is not None:
				setattr(self, attr, get_list(attr, value, vtype, ","))

		def commas_or_string(attr: str, vtype: Any) -> None:
			value = getattr(args, attr)

			if value is not None:
				if "," in value:
					setattr(self, attr, get_list(attr, value, vtype, ","))
				else:
					setattr(self, attr, value)

		def path(attr: str) -> None:
			value = getattr(args, attr)

			if value is not None:
				setattr(self, attr, utils.resolve_path(value))

		def pathlist(attr: str) -> None:
			value = getattr(args, attr)

			if value is not None:
				paths = [utils.resolve_path(p.strip()) for p in value.split(",")]
				setattr(self, attr, paths)

		# Allow p1 and m1 formats
		def number(attr: str, vtype: Any, allow_zero: bool) -> None:
			default = getattr(self, attr)
			value = getattr(args, attr)

			if value is None:
				return

			value = str(value)
			num = value
			op = ""

			if value.startswith("p") or value.startswith("m"):
				op = value[0]
				num = value[1:]

			try:
				if vtype == int:
					num = int(num)
				elif vtype == float:
					num = float(num)
			except:
				utils.exit(f"Failed to parse '{attr}'")
				return

			if op == "p":
				num = default + num
			elif op == "m":
				num = default - num

			err = f"Value for '{attr}' is too low"

			if num == 0:
				if not allow_zero:
					utils.exit(err)
			elif num < 0:
				utils.exit(err)
				return

			setattr(self, attr, num)

		# ---------

		path("script")
		self.check_script(args)

		normal("left")
		normal("right")
		normal("top")
		normal("bottom")
		normal("width")
		normal("height")
		normal("format")
		normal("order")
		normal("font")
		normal("frames")
		normal("loop")
		normal("separator")
		normal("filter")
		normal("remake")
		normal("repeatrandom")
		normal("repeatfilter")
		normal("fillwords")
		normal("nogrow")
		normal("align")

		number("fontsize", int, False)
		number("delay", int, False)
		number("opacity", float, True)
		number("padding", int, True)
		number("radius", int, True)
		number("outlinewidth", int, False)
		number("wrap", int, False)

		commas_or_string("fontcolor", int)
		commas_or_string("bgcolor", int)
		commas_or_string("outline", int)
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
			return [codecs.decode(utils.clean_lines(item), "unicode-escape") \
			 for item in value.split(self.separator)]

		for path in self.input:
			if not path.exists() or not path.is_file():
				utils.exit("Input file does not exist")
				return

		if self.wordfile:
			if not self.wordfile.exists() or not self.wordfile.is_file():
				utils.exit("Word file does not exist")
				return

			self.read_wordfile()
		elif args.words:
			self.words = separate(args.words)

		if args.randomlist:
			self.randomlist = separate(args.randomlist)

		if not self.randomfile.exists() or not self.randomfile.is_file():
			utils.exit("Word file does not exist")
			return

		self.linebreaks("words")
		self.set_color("fontcolor")
		self.set_color("bgcolor")
		self.set_color("outline")

	def linebreaks(self, attr: str) -> None:
		lines = getattr(self, attr)

		if not lines:
			return

		new_lines = []

		for line in lines:
			lines = line.split("\n")
			wrapped = [textwrap.fill(x, self.wrap) for x in lines]
			new_lines.append("\n".join(wrapped))

		setattr(self, attr, new_lines)

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