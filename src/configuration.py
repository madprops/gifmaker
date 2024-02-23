# Modules
import utils
from argparser import ArgParser

# Standard
import codecs
import textwrap
from argparse import Namespace
from typing import List, Union, Dict, Tuple, Any
from pathlib import Path


class Configuration:
    # Class to hold all the configuration of the program
    # It also interfaces with ArgParser and processes further

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

    # Dont' draw the left outline
    noleftoutline = False

    # Don't draw the right outline
    norightoutline = False

    # Don't draw the top outline
    notopoutline = False

    # Don't draw the bottom outline
    nobottomoutline = False

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
    wrap = 35

    # Don't wrap lines
    nowrap = False

    # --- INTERAL VARS

    # List to keep track of used random words
    randwords: List[str] = []

    # Counter for [count]
    wordcount = 0

    # Last font color used
    last_fontcolor = Union[Tuple[int, int, int], None]

    def get_argdefs(self) -> Tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
        rgbstr = "3 numbers from 0 to 255, separated by commas. Names like 'yellow' are also supported"
        commastr = "Separated by commas"

        argdefs: List[Dict[str, Any]] = [
            {"name": "input", "type": str,
             "help": "Path to the a video or image file. Separated by commas"},

            {"name": "words", "type": str,
             "help": "Lines of words to use on the frames"},

            {"name": "wordfile", "type": str,
             "help": "Path of file with word lines"},

            {"name": "delay", "type": str,
             "help": "The delay in ms between frames"},

            {"name": "left", "type": int,
             "help": "Left padding"},

            {"name": "right", "type": int,
             "help": "Right padding"},

            {"name": "top", "type": int,
             "help": "Top padding"},

            {"name": "bottom", "type": int,
             "help": "Bottom padding"},

            {"name": "width", "type": int,
             "help": "Width to resize the frames"},

            {"name": "height", "type": int,
             "help": "Height to resize the frames"},

            {"name": "frames", "type": int,
             "help": "Number of frames to use if no words are provided"},

            {"name": "output", "type": str,
             "help": "Output directory to save the file"},

            {"name": "format", "type": str,
             "choices": ["gif", "webm", "mp4", "jpg", "png"],
             "help": "The format of the output file"},

            {"name": "separator", "type": str,
             "help": "Character to use as the separator"},

            {"name": "order", "type": str,
             "choices": ["random", "normal"],
             "help": "The order to use when extracting the frames"},

            {"name": "font", "type": str,
             "choices": ["sans", "serif", "mono", "bold", "italic", "cursive", "comic"],
             "help": "The font to use for the text"},

            {"name": "fontsize", "type": str,
             "help": "The size of the font"},

            {"name": "fontcolor", "type": str,
             "help": f"Text color. {rgbstr}"},

            {"name": "bgcolor", "type": str,
             "help": f"Add a background rectangle for the text with this color. {rgbstr}"},

            {"name": "outline", "type": str,
             "help": f"Add an outline around the text with this color. {rgbstr}"},

            {"name": "outlinewidth", "type": str,
             "help": "The width of the outline"},

            {"name": "opacity", "type": str,
             "help": "The opacity of the background rectangle"},

            {"name": "padding", "type": str,
             "help": "The padding of the background rectangle"},

            {"name": "radius", "type": str,
             "help": "The border radius of the background"},

            {"name": "align", "type": str,
             "choices": ["left", "center", "right"],
             "help": "How to align the center when there are multiple lines"},

            {"name": "randomlist", "type": str,
             "help": "List of words to consider for random words"},

            {"name": "randomfile", "type": str,
             "help": "Path to a list of words to consider for random words"},

            {"name": "script", "type": str,
             "help": "Path to a TOML file that defines the arguments to use"},

            {"name": "loop", "type": int,
             "help": "How to loop a gif render"},

            {"name": "remake", "action": "store_true",
             "help": "Re-render the frames to change the width or delay"},

            {"name": "filter", "type": str,
             "choices": ["hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8", "anyhue", "anyhue2",
                         "gray", "blur", "invert", "random", "random2", "none"],
             "help": "Color filter to apply to frames"},

            {"name": "filterlist", "type": str,
             "help": f"Filters to use per frame. {commastr}"},

            {"name": "filteropts", "type": str,
             "help": f"The list of allowed filters when picking randomly. {commastr}"},

            {"name": "framelist", "type": str,
             "help": f"List of frame indices to use. {commastr}"},

            {"name": "repeatrandom", "action": "store_true",
             "help": "Repeating random words is ok"},

            {"name": "repeatfilter", "action": "store_true",
             "help": "Repeating random filters is ok"},

            {"name": "fillwords", "action": "store_true",
             "help": "Fill the rest of the frames with the last word line"},

            {"name": "nogrow", "action": "store_true",
             "help": "Don't resize if the frames are going to be bigger than the original"},

            {"name": "wrap", "type": str,
             "help": "Split line if it exceeds this char length"},

            {"name": "nowrap", "action": "store_true",
             "help": "Don't wrap lines"},

            {"name": "noleftoutline", "action": "store_true",
             "help": "Don't draw the left outline"},

            {"name": "norightoutline", "action": "store_true",
             "help": "Don't draw the right outline"},

            {"name": "notopoutline", "action": "store_true",
             "help": "Don't draw the top outline"},

            {"name": "nobottomoutline", "action": "store_true",
             "help": "Don't draw the bottom outline"},
        ]

        aliases = {
            "input": ["--i", "-i"],
            "output": ["--o", "-o"],
        }

        return argdefs, aliases

    def parse_args(self) -> None:
        argdefs, aliases = self.get_argdefs()
        ap = ArgParser("Gif Maker", argdefs, aliases, self)

        # ---

        ap.path("script")
        self.check_script(ap.args)

        # ---

        ap.number("fontsize", int)
        ap.number("delay", int, duration=True)
        ap.number("opacity", float, allow_zero=True)
        ap.number("padding", int, allow_zero=True)
        ap.number("radius", int, allow_zero=True)
        ap.number("outlinewidth", int)
        ap.number("wrap", int)

        # ---

        ap.commas("filterlist", str)
        ap.commas("filteropts", str)
        ap.commas("framelist", int)
        ap.commas("fontcolor", int, allow_string=True)
        ap.commas("bgcolor", int, allow_string=True)
        ap.commas("outline", int, allow_string=True)

        # ---

        normals = ["left", "right", "top", "bottom", "width", "height", "format", "order",
                   "font", "frames", "loop", "separator", "filter", "remake", "repeatrandom",
                   "repeatfilter", "fillwords", "nogrow", "align", "nowrap", "noleftoutline",
                   "norightoutline", "notopoutline", "nobottomoutline"]

        for normal in normals:
            ap.normal(normal)

        # ---

        paths = ["output", "wordfile", "randomfile"]

        for path in paths:
            ap.path(path)

        # ---

        pathlists = ["input"]

        for pathlist in pathlists:
            ap.pathlist(pathlist)

        # ---

        self.check_config(ap.args)

    def check_config(self, args: Namespace) -> None:
        def separate(value: str) -> List[str]:
            return [codecs.decode(utils.clean_lines(item), "unicode-escape")
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

        if not self.nowrap:
            self.wrap_text("words")

        self.set_color("fontcolor")
        self.set_color("bgcolor")
        self.set_color("outline")

    def wrap_text(self, attr: str) -> None:
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
        if self.wordfile:
            self.words = self.wordfile.read_text().splitlines()

    def fill_paths(self, main_file: str) -> None:
        self.root = utils.full_path(Path(main_file).parent.parent)
        self.input = [utils.full_path(Path(self.root, "media", "video.webm"))]
        self.output = utils.full_path(Path(self.root, "output"))
        self.randomfile = utils.full_path(Path(self.root, "data", "nouns.txt"))
        self.fontspath = utils.full_path(Path(self.root, "fonts"))


# Main configuration object
config = Configuration()
