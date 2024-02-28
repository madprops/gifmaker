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
        self.colorseed: Union[int, None] = None
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

        # Strings for info
        rgbstr = "3 numbers from 0 to 255, separated by commas. Names like 'yellow' are also supported"
        commastr = "Separated by commas"

        # Argument definitions
        argdefs: Dict[str, Any] = {
            "input": {"value": None, "type": str, "help": "Path to a video or image file. Separated by commas"},
            "words": {"value": [], "type": str, "help": "Lines of words to use on the frames"},
            "wordfile": {"value": None, "type": str, "help": "Path of file with word lines"},
            "delay": {"value": 700, "type": str, "help": "The delay in ms between frames"},
            "left": {"value": None, "type": int, "help": "Left padding"},
            "right": {"value": None, "type": int, "help": "Right padding"},
            "top": {"value": None, "type": int, "help": "Top padding"},
            "bottom": {"value": None, "type": int, "help": "Bottom padding"},
            "width": {"value": None, "type": int, "help": "Width to resize the frames"},
            "height": {"value": None, "type": int, "help": "Height to resize the frames"},
            "frames": {"value": None, "type": int, "help": "Number of frames to use if no words are provided"},
            "output": {"value": None, "type": str, "help": "Output directory to save the file"},
            "format": {"value": "gif", "type": str, "choices": ["gif", "webm", "mp4", "jpg", "png"], "help": "The format of the output file"},
            "separator": {"value": ";", "type": str, "help": "Character to use as the separator"},
            "order": {"value": "random", "type": str, "choices": ["random", "normal"], "help": "The order to use when extracting the frames"},
            "font": {"value": "sans", "type": str, "help": "The font to use for the text"},
            "fontsize": {"value": 60, "type": str, "help": "The size of the font"},
            "fontcolor": {"value": (255, 255, 255), "type": str, "help": f"Text color. {rgbstr}"},
            "bgcolor": {"value": None, "type": str, "help": f"Add a background rectangle for the text with this color. {rgbstr}"},
            "outline": {"value": None, "type": str, "help": f"Add an outline around the text with this color. {rgbstr}"},
            "outlinewidth": {"value": 2, "type": str, "help": "The width of the outline"},
            "opacity": {"value": 0.66, "type": str, "help": "The opacity of the background rectangle"},
            "padding": {"value": 20, "type": str, "help": "The padding of the background rectangle"},
            "radius": {"value": 0, "type": str, "help": "The border radius of the background"},
            "align": {"value": "center", "type": str, "choices": ["left", "center", "right"], "help": "How to align the center when there are multiple lines"},
            "randomlist": {"value": [], "type": str, "help": "List of words to consider for random words"},
            "randomfile": {"value": None, "type": str, "help": "Path to a list of words to consider for random words"},
            "script": {"value": None, "type": str, "help": "Path to a TOML file that defines the arguments to use"},
            "loop": {"value": 0, "type": int, "help": "How to loop a gif render"},
            "remake": {"value": False, "action": "store_true", "help": "Re-render the frames to change the width or delay"},
            "filter": {"value": "none", "type": str,
                       "help": "Color filter to apply to frames",
                       "choices": ["hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8",
                                   "anyhue", "anyhue2", "gray", "grey", "blur", "invert", "random", "random2", "none"]},
            "filterlist": {"value": [], "type": str, "help": f"Filters to use per frame. {commastr}"},
            "filteropts": {"value": [], "type": str, "help": f"The list of allowed filters when picking randomly. {commastr}"},
            "framelist": {"value": [], "type": str, "help": f"List of frame indices to use. {commastr}"},
            "frameopts": {"value": [], "type": str, "help": f"The list of allowed frame indices when picking randomly. {commastr}"},
            "repeatrandom": {"value": False, "action": "store_true", "help": "Repeating random words is ok"},
            "repeatfilter": {"value": False, "action": "store_true", "help": "Repeating random filters is ok"},
            "fillwords": {"value": False, "action": "store_true", "help": "Fill the rest of the frames with the last word line"},
            "fillgen": {"value": False, "action": "store_true", "help": "Generate the first line of words till the end of frames"},
            "nogrow": {"value": False, "action": "store_true", "help": "Don't resize if the frames are going to be bigger than the original"},
            "wrap": {"value": 35, "type": str, "help": "Split line if it exceeds this char length"},
            "nowrap": {"value": False, "action": "store_true", "help": "Don't wrap lines"},
            "no_outline_left": {"value": False, "action": "store_true", "help": "Don't draw the left outline"},
            "no_outline_right": {"value": False, "action": "store_true", "help": "Don't draw the right outline"},
            "no_outline_top": {"value": False, "action": "store_true", "help": "Don't draw the top outline"},
            "no_outline_bottom": {"value": False, "action": "store_true", "help": "Don't draw the bottom outline"},
            "verbose": {"value": False, "action": "store_true", "help": "Print more information like time performance"},
            "descender": {"value": False, "action": "store_true", "help": "Apply the height of the descender to the bottom padding of the text"},
            "seed": {"value": None, "type": int, "help": "Seed to use when using any random value"},
            "frameseed": {"value": None, "type": int, "help": "Seed to use when picking frames"},
            "wordseed": {"value": None, "type": int, "help": "Seed to use when picking words"},
            "filterseed": {"value": None, "type": int, "help": "Seed to use when picking filters"},
            "colorseed": {"value": None, "type": int, "help": "Seed to use when picking colors"},
            "deepfry": {"value": False, "action": "store_true", "help": "Compress the frames heavily"},
            "vertical": {"value": False, "action": "store_true", "help": "Append images vertically"},
            "horizontal": {"value": False, "action": "store_true", "help": "Append images horizontally"},
            "mode": {"value": "normal", "type": str, "help": "Use 'arginfo' to print the argument information."},
        }

        aliases = {
            "input": ["--i", "-i"],
            "output": ["--o", "-o"],
        }

    def parse_args(self) -> None:
        ap = ArgParser("Gif Maker", self.Internal.argdefs, self.Internal.aliases, self)

        # ---

        ap.normal("mode")

        if self.mode == "arginfo":
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
                   "descender", "seed", "frameseed", "wordseed", "filterseed", "colorseed",
                   "deepfry", "vertical", "horizontal"]

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
        set_rng("colorseed", "random_colors")

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
        new_dict = {
            key: {k: v for k, v in value.items() if (k != "type" and k != "action")}
            for key, value in self.Internal.argdefs.items()
        }

        return json.dumps(new_dict)


# Main configuration object
config = Configuration()
