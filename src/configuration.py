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

        aliases = {
            "input": ["--i", "-i"],
            "output": ["--o", "-o"],
        }

        # Strings for info
        rgbstr = "3 numbers from 0 to 255, separated by commas. Names like 'yellow' are also supported"
        commastr = "Separated by commas"

    # Argument definitions
    arguments: Dict[str, Any] = {
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
        "fontcolor": {"value": (255, 255, 255), "type": str, "help": f"Text color. {Internal.rgbstr}"},
        "bgcolor": {"value": None, "type": str, "help": f"Add a background rectangle for the text with this color. {Internal.rgbstr}"},
        "outline": {"value": None, "type": str, "help": f"Add an outline around the text with this color. {Internal.rgbstr}"},
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
        "filter": {"value": "none", "type": str, "help": "Color filter to apply to frames"},
        "filterlist": {"value": [], "type": str, "help": f"Filters to use per frame. {Internal.commastr}"},
        "filteropts": {"value": [], "type": str, "help": f"The list of allowed filters when picking randomly. {Internal.commastr}"},
        "framelist": {"value": [], "type": str, "help": f"List of frame indices to use. {Internal.commastr}"},
        "frameopts": {"value": [], "type": str, "help": f"The list of allowed frame indices when picking randomly. {Internal.commastr}"},
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
        "mode": {"value": "normal", "type": str, "help": "Use 'defaults' to print the default values."},
    }

    def get(self, attr: str) -> Any:
        return self.arguments[attr]["value"]

    def set(self, attr: str, value: Any) -> None:
        self.arguments[attr]["value"] = value

    def parse_args(self) -> None:
        ap = ArgParser("Gif Maker", self.arguments, self.Internal.aliases, self)

        # ---

        ap.normal("mode")

        if self.get("mode") == "defaults":
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
                    for item in value.split(self.get("separator"))]

        if (not self.get("input").exists()) or (not self.get("input").is_file()):
            utils.exit("Input file does not exist")
            return

        if self.get("wordfile"):
            if not self.get("wordfile").exists() or not self.get("wordfile").is_file():
                utils.exit("Word file does not exist")
                return

            self.read_wordfile()
        elif args.words:
            self.set("words", separate(args.words))

        if args.randomlist:
            self.set("randomlist", separate(args.randomlist))

        if not self.get("randomfile").exists() or not self.get("randomfile").is_file():
            utils.exit("Word file does not exist")
            return

        if not self.get("nowrap"):
            self.wrap_text("words")

        if self.get("vertical") or self.get("horizontal"):
            if self.get("format") not in ["jpg", "png"]:
                self.set("format", "png")

        self.set_random()

    def wrap_text(self, attr: str) -> None:
        lines = self.get(attr)

        if not lines:
            return

        new_lines = []

        for line in lines:
            lines = line.split("\n")
            wrapped = [textwrap.fill(x, self.get("wrap")) for x in lines]
            new_lines.append("\n".join(wrapped))

        self.set(attr, new_lines)

    def check_script(self, args: Namespace) -> None:
        if self.get("script") is None:
            return

        data = utils.read_toml(Path(self.get("script")))

        if data:
            for key in data:
                k = utils.dash_to_under(key)
                setattr(args, k, data[key])

    def read_wordfile(self) -> None:
        if self.get("wordfile"):
            self.set("words", self.wordfile.read_text().splitlines())

    def fill_root(self, main_file: str) -> None:
        self.Internal.root = Path(main_file).parent.parent
        self.Internal.fontspath = utils.full_path(Path(self.Internal.root, "fonts"))

    def fill_paths(self) -> None:
        if not self.get("input"):
            self.set("input", utils.full_path(Path(self.Internal.root, "media", "video.webm")))

        if not self.get("output"):
            self.set("output", utils.full_path(Path(self.Internal.root, "output")))

        if not self.get("randomfile"):
            self.set("randomfile", utils.full_path(Path(self.Internal.root, "data", "nouns.txt")))

    def get_color(self, attr: str) -> Tuple[int, int, int]:
        value = self.get(attr)
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
            self.set(attr, rgb)

        return ans

    def set_random(self) -> None:
        def set_rng(attr: str, rng_name: str) -> None:
            value = self.get(attr)

            if value is not None:
                rand = random.Random(value)
            elif self.get("seed") is not None:
                rand = random.Random(self.get("seed"))
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

        if self.get("font") == "random":
            font = random_font()
            font_file = fonts[font]
            self.set("font", font)
        elif self.get("font") == "random2":
            font = random_font()
            font_file = fonts[font]
        elif ".ttf" in self.get("font"):
            font_file = str(utils.resolve_path(Path(self.get("font"))))
        elif self.get("font") in fonts:
            font_file = fonts[self.get("font")]
        else:
            font_file = fonts["sans"]

        path = Path(self.Internal.fontspath, font_file)
        return ImageFont.truetype(path, size=self.get("fontsize"))

    def to_json(self) -> str:
        new_dict = {
            key: {k: v for k, v in value.items() if (k != "type" and k != "action")}
            for key, value in self.arguments.items()
        }

        return json.dumps(new_dict)


# Main configuration object
config = Configuration()
