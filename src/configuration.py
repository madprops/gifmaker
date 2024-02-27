# Modules
import utils
from argparser import ArgParser

# Standard
import json
import codecs
import textwrap
import random
from argparse import Namespace
from typing import List, Union, Dict, Tuple, Any
from PIL import ImageFont  # type: ignore
from pathlib import Path


class Configuration:
    # Class to hold all the configuration of the program
    # It also interfaces with ArgParser and processes further

    def __init__(self) -> None:
        self.delay = 700
        self.input: Union[Path, None] = None
        self.output: Union[Path, None] = None
        self.randomfile: Union[Path, None] = None
        self.frames: Union[int, None] = None
        self.left: Union[int, None] = None
        self.right: Union[int, None] = None
        self.top: Union[int, None] = None
        self.bottom: Union[int, None] = None
        self.width: Union[int, None] = None
        self.height: Union[int, None] = None
        self.words: List[str] = []
        self.wordfile: Union[Path, None] = None
        self.randomlist: List[str] = []
        self.separator = ";"
        self.format = "gif"
        self.order = "random"
        self.font = "sans"
        self.fontsize = 60
        self.fontcolor: Union[Tuple[int, int, int], str] = (255, 255, 255)
        self.bgcolor: Union[Tuple[int, int, int], str, None] = None
        self.outline: Union[Tuple[int, int, int], str, None] = None
        self.outlinewidth = 2
        self.no_outline_left = False
        self.no_outline_right = False
        self.no_outline_top = False
        self.no_outline_bottom = False
        self.opacity = 0.66
        self.padding = 20
        self.radius = 0
        self.align = "center"
        self.script: Union[Path, None] = None
        self.loop = 0
        self.remake = False
        self.filterlist: List[str] = []
        self.filteropts: List[str] = []
        self.filter = "none"
        self.framelist: List[str] = []
        self.frameopts: List[str] = []
        self.repeatrandom = False
        self.repeatfilter = False
        self.fillwords = False
        self.fillgen = False
        self.nogrow = False
        self.wrap = 35
        self.nowrap = False
        self.verbose = False
        self.descender = False
        self.seed: Union[int, None] = None
        self.frameseed: Union[int, None] = None
        self.wordseed: Union[int, None] = None
        self.filterseed: Union[int, None] = None
        self.deepfry = False
        self.vertical = False
        self.horizontal = False
        self.mode = "normal"

    class Internal:
        # The path where the main file is located
        root: Union[Path, None] = None

        # The path where the fonts are located
        fontspath: Union[Path, None] = None

        # List to keep track of used random words
        randwords: List[str] = []

        # Counter for [count]
        wordcount = 0

        # Last font color used
        last_fontcolor: Union[Tuple[int, int, int], None] = None

        # Random generators
        random_frames: Union[random.Random, None] = None
        random_words: Union[random.Random, None] = None
        random_filters: Union[random.Random, None] = None

        # Data of some modes
        data = ""

        # Choices for some arguments
        choices = {
            "format": ["gif", "webm", "mp4", "jpg", "png"],
            "order": ["random", "normal"],
            "align": ["left", "center", "right"],
            "filter": ["hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8", "anyhue", "anyhue2",
                        "gray", "grey", "blur", "invert", "random", "random2", "none"],
        }

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
             "choices": self.Internal.choices["format"],
             "help": "The format of the output file"},

            {"name": "separator", "type": str,
             "help": "Character to use as the separator"},

            {"name": "order", "type": str,
             "choices": self.Internal.choices["order"],
             "help": "The order to use when extracting the frames"},

            {"name": "font", "type": str,
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
             "choices": self.Internal.choices["align"],
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
             "choices": self.Internal.choices["filter"],
             "help": "Color filter to apply to frames"},

            {"name": "filterlist", "type": str,
             "help": f"Filters to use per frame. {commastr}"},

            {"name": "filteropts", "type": str,
             "help": f"The list of allowed filters when picking randomly. {commastr}"},

            {"name": "framelist", "type": str,
             "help": f"List of frame indices to use. {commastr}"},

            {"name": "frameopts", "type": str,
             "help": f"The list of allowed frame indices when picking randomly. {commastr}"},

            {"name": "repeatrandom", "action": "store_true",
             "help": "Repeating random words is ok"},

            {"name": "repeatfilter", "action": "store_true",
             "help": "Repeating random filters is ok"},

            {"name": "fillwords", "action": "store_true",
             "help": "Fill the rest of the frames with the last word line"},

            {"name": "fillgen", "action": "store_true",
             "help": "Generate the first line of words till the end of frames"},

            {"name": "nogrow", "action": "store_true",
             "help": "Don't resize if the frames are going to be bigger than the original"},

            {"name": "wrap", "type": str,
             "help": "Split line if it exceeds this char length"},

            {"name": "nowrap", "action": "store_true",
             "help": "Don't wrap lines"},

            {"name": "no-outline-left", "action": "store_true",
             "help": "Don't draw the left outline"},

            {"name": "no-outline-right", "action": "store_true",
             "help": "Don't draw the right outline"},

            {"name": "no-outline-top", "action": "store_true",
             "help": "Don't draw the top outline"},

            {"name": "no-outline-bottom", "action": "store_true",
             "help": "Don't draw the bottom outline"},

            {"name": "verbose", "action": "store_true",
             "help": "Print more information like time performance"},

            {"name": "descender", "action": "store_true",
             "help": "Apply the height of the descender to the bottom padding of the text"},

            {"name": "seed", "type": int,
             "help": "Seed to use when using any random value"},

            {"name": "frameseed", "type": int,
             "help": "Seed to use when picking frames"},

            {"name": "wordseed", "type": int,
             "help": "Seed to use when picking words"},

            {"name": "filterseed", "type": int,
             "help": "Seed to use when picking filters"},

            {"name": "deepfry", "action": "store_true",
             "help": "Compress the frames heavily"},

            {"name": "vertical", "action": "store_true",
             "help": "Append images vertically"},

            {"name": "horizontal", "action": "store_true",
             "help": "Append images horizontally"},

            {"name": "mode", "type": str,
             "help": "Use 'defaults' to print the default values."},
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

        ap.normal("mode")

        if self.mode == "defaults":
            self.Internal.data = self.to_json()
            return

        # ---

        ap.path("script")
        self.check_script(ap.args)

        # ---

        string_arg = ap.string_arg()

        if string_arg:
            ap.args.words = string_arg

        # ---

        ap.number("fontsize", int)
        ap.number("delay", int, duration=True)
        ap.number("opacity", float, allow_zero=True)
        ap.number("padding", int, allow_zero=True)
        ap.number("radius", int, allow_zero=True)
        ap.number("outlinewidth", int)
        ap.number("wrap", int)

        # ---

        ap.commas("framelist", int)
        ap.commas("frameopts", int)
        ap.commas("filterlist", str)
        ap.commas("filteropts", str)
        ap.commas("fontcolor", int, allow_string=True, is_tuple=True)
        ap.commas("bgcolor", int, allow_string=True, is_tuple=True)
        ap.commas("outline", int, allow_string=True, is_tuple=True)

        # ---

        normals = ["left", "right", "top", "bottom", "width", "height", "format", "order",
                   "font", "frames", "loop", "separator", "filter", "remake", "repeatrandom",
                   "repeatfilter", "fillwords", "nogrow", "align", "nowrap", "no_outline_left",
                   "no_outline_right", "no_outline_top", "no_outline_bottom", "verbose", "fillgen",
                   "descender", "seed", "frameseed", "wordseed", "filterseed", "deepfry",
                   "vertical", "horizontal"]

        for normal in normals:
            ap.normal(normal)

        # ---

        paths = ["input", "output", "wordfile", "randomfile"]

        for path in paths:
            ap.path(path)

        # ---

        self.fill_paths()
        self.check_config(ap.args)

    def check_config(self, args: Namespace) -> None:
        def separate(value: str) -> List[str]:
            return [codecs.decode(utils.clean_lines(item), "unicode-escape")
                    for item in value.split(self.separator)]

        assert isinstance(self.input, Path)

        if (not self.input.exists()) or (not self.input.is_file()):
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

        assert isinstance(self.randomfile, Path)

        if not self.randomfile.exists() or not self.randomfile.is_file():
            utils.exit("Word file does not exist")
            return

        if not self.nowrap:
            self.wrap_text("words")

        if self.vertical or self.horizontal:
            if self.format not in ["jpg", "png"]:
                self.format = "png"

        self.set_random()

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

    def check_script(self, args: Namespace) -> None:
        if self.script is None:
            return

        data = utils.read_toml(Path(self.script))

        if data:
            for key in data:
                k = utils.dash_to_under(key)
                setattr(args, k, data[key])

    def read_wordfile(self) -> None:
        if self.wordfile:
            self.words = self.wordfile.read_text().splitlines()

    def fill_root(self, main_file: str) -> None:
        self.Internal.root = Path(main_file).parent.parent
        self.Internal.fontspath = utils.full_path(Path(self.Internal.root, "fonts"))

    def fill_paths(self) -> None:
        assert isinstance(self.Internal.root, Path)

        if not self.input:
            self.input = utils.full_path(Path(self.Internal.root, "media", "video.webm"))

        if not self.output:
            self.output = utils.full_path(Path(self.Internal.root, "output"))

        if not self.randomfile:
            self.randomfile = utils.full_path(Path(self.Internal.root, "data", "nouns.txt"))

    def get_color(self, attr: str) -> Tuple[int, int, int]:
        value = getattr(self, attr)
        rgb: Union[Tuple[int, int, int], None] = None
        set_config = False

        if isinstance(value, str):
            if value == "light":
                rgb = utils.random_light()
                set_config = True
            elif value == "light2":
                rgb = utils.random_light()
            elif value == "dark":
                rgb = utils.random_dark()
                set_config = True
            elif value == "dark2":
                rgb = utils.random_dark()
            elif (value == "font") and isinstance(self.Internal.last_fontcolor, tuple):
                rgb = self.Internal.last_fontcolor
            elif value == "lightfont" and isinstance(self.Internal.last_fontcolor, tuple):
                rgb = utils.light_contrast(self.Internal.last_fontcolor)
                set_config = True
            elif value == "lightfont2" and isinstance(self.Internal.last_fontcolor, tuple):
                rgb = utils.light_contrast(self.Internal.last_fontcolor)
            elif value == "darkfont" and isinstance(self.Internal.last_fontcolor, tuple):
                rgb = utils.dark_contrast(self.Internal.last_fontcolor)
                set_config = True
            elif value == "darkfont2" and isinstance(self.Internal.last_fontcolor, tuple):
                rgb = utils.dark_contrast(self.Internal.last_fontcolor)
            else:
                rgb = utils.color_name(value)
        elif isinstance(value, (list, tuple)) and len(value) >= 3:
            rgb = (value[0], value[1], value[2])

        ans = rgb or (100, 100, 100)

        if attr == "fontcolor":
            self.Internal.last_fontcolor = ans

        if set_config:
            setattr(self, attr, rgb)

        return ans

    def set_random(self) -> None:
        def set_rng(attr: str, rng_name: str) -> None:
            value = getattr(self, attr)

            if value is not None:
                rand = random.Random(value)
            elif self.seed is not None:
                rand = random.Random(self.seed)
            else:
                rand = random.Random()

            setattr(self.Internal, rng_name, rand)

        set_rng("frameseed", "random_frames")
        set_rng("wordseed", "random_words")
        set_rng("filterseed", "random_filters")

    def get_font(self) -> ImageFont.FreeTypeFont:
        fonts = {
            "sans": "Roboto-Regular.ttf",
            "serif": "RobotoSerif-Regular.ttf",
            "mono": "RobotoMono-Regular.ttf",
            "italic": "Roboto-Italic.ttf",
            "bold": "Roboto-Bold.ttf",
            "cursive": "Pacifico-Regular.ttf",
            "comic": "ComicNeue-Regular.ttf",
            "nova": "NovaSquare-Regular.ttf",
        }

        def random_font() -> str:
            return random.choice(list(fonts.keys()))

        if self.font == "random":
            font = random_font()
            font_file = fonts[font]
            self.font = font
        elif self.font == "random2":
            font = random_font()
            font_file = fonts[font]
        elif ".ttf" in self.font:
            font_file = str(utils.resolve_path(Path(self.font)))
        elif self.font in fonts:
            font_file = fonts[self.font]
        else:
            font_file = fonts["sans"]

        assert isinstance(self.Internal.fontspath, Path)
        path = Path(self.Internal.fontspath, font_file)
        return ImageFont.truetype(path, size=self.fontsize)

    def to_json(self) -> str:
        jsondict = {}

        for key in self.__dict__:
            value = getattr(self, key)

            if isinstance(value, Path):
                value = str(value)

            jsondict[key] = value

        for key in self.Internal.choices:
            value = self.Internal.choices[key]
            jsondict[f"_choices_{key}"] = value

        return json.dumps(jsondict)


# Main configuration object
config = Configuration()
