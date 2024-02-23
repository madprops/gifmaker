# Standard
import re
import sys
import random
import string
import colorsys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Union, Tuple

# Libraries
import webcolors  # type: ignore

# Used for random colors
colordiff = 0.15


def random_string() -> str:
    vowels = "aeiou"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))

    def con() -> str:
        return random.choice(consonants)

    def vow() -> str:
        return random.choice(vowels)

    return con() + vow() + con() + vow() + con() + vow()


def get_extension(path: Path) -> str:
    return Path(path).suffix.lower().lstrip(".")


def resolve_path(path: Path) -> Path:
    pth = Path(path).expanduser()

    if pth.is_absolute():
        return full_path(pth)
    else:
        return full_path(Path(Path.cwd(), pth))


def full_path(path: Path) -> Path:
    return path.expanduser().resolve()


def exit(message: str) -> None:
    print(f"\nExit: {message}\n")
    sys.exit(1)


def read_toml(path: Path) -> Union[Dict[str, str], None]:
    import tomllib

    if (not path.exists()) or (not path.is_file()):
        exit("TOML file does not exist")
        return None

    try:
        return tomllib.load(open(path, "rb"))
    except Exception as e:
        print(f"Error: {e}")
        exit("Failed to read TOML file")
        return None


def random_color(lightness: float) -> Tuple[int, int, int]:
    hue = random.random()
    saturation = 0.8
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, lightness)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def random_light() -> Tuple[int, int, int]:
    return random_color(1 - colordiff)


def random_dark() -> Tuple[int, int, int]:
    return random_color(colordiff)


def random_digit(allow_zero: bool) -> int:
    if allow_zero:
        return random.randint(0, 9)
    else:
        return random.randint(1, 9)


def get_date(fmt: str) -> str:
    if fmt:
        return datetime.now().strftime(fmt)
    else:
        return str(int(datetime.now().timestamp()))


def add_alpha(rgb: Tuple[int, int, int], alpha: float) -> Tuple[int, int, int, int]:
    return int(rgb[0]), int(rgb[1]), int(rgb[2]), int(255 * alpha)


def color_name(name: str) -> Union[Tuple[int, int, int], None]:
    try:
        return tuple(webcolors.name_to_rgb(name))
    except:
        return None


def clean_lines(s: str) -> str:
    cleaned = s
    cleaned = re.sub(r" *(\n|\\n) *", "\n", cleaned)
    cleaned = re.sub(r" +", " ", cleaned)
    return cleaned.strip()


def parse_duration(time_string: str) -> str:
    match = re.match(r"(\d+(\.\d+)?)([smh]+)", time_string)

    if match:
        value, _, unit = match.groups()
        value = float(value)

        if unit == "ms":
            time_string = str(int(value))
        elif unit == "s":
            time_string = str(int(value * 1000))
        elif unit == "m":
            time_string = str(int(value * 60 * 1000))
        elif unit == "h":
            time_string = str(int(value * 60 * 60 * 1000))

    return time_string


def divisible(number, by):
    while number % by != 0:
        number += 1

    return number
