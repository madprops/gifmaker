# Modules
from configuration import config
import utils

# Standard
import re
from typing import List, Any


def process_words() -> None:
    if config.remake or config.fillgen:
        return

    check_empty()
    check_generators()
    check_repeat()


def check_generators() -> None:
    if not config.words:
        return

    new_lines: List[str] = []

    for line in config.words:
        new_lines.extend(generate(line))

    config.words = new_lines


def generate(line: str, multiple: bool = True) -> List[str]:
    def randgen(word: str, num: int) -> List[str]:
        items: List[str] = []

        for _ in range(num):
            allow_zero = True

            if num > 1:
                if len(items) == 0:
                    allow_zero = False

            items.append(get_random(word, allow_zero))

        return items

    def replace_random(match: re.Match[Any]) -> str:
        num = None

        if match["number"]:
            num = int(match["number"])

        if (num is None) or (num < 1):
            num = 1

        return " ".join(randgen("random", num))

    def replace_number(match: re.Match[Any]) -> str:
        num1 = None
        num2 = None

        if match["number1"]:
            num1 = int(match["number1"])

        if match["number2"]:
            num2 = int(match["number2"])

        if num1 is not None and num2 is not None:
            return str(config.random_words.randint(num1, num2))

        if (num1 is None) or (num1 < 1):
            num1 = 1

        return "".join(randgen("number", num1))

    def replace_count(match: re.Match[Any]) -> str:
        config.wordcount += 1
        return str(config.wordcount)

    def replace_date(match: re.Match[Any]) -> str:
        fmt = match["format"] or "%H:%M:%S"
        return utils.get_date(fmt)

    multi = 1
    new_lines: List[str] = []
    pattern_multi = re.compile(r"\[\s*(?:x(?P<number>\d+))?\s*\]$", re.IGNORECASE)

    if multiple:
        match_multi = re.search(pattern_multi, line)

        if match_multi:
            multi = max(1, int(match_multi["number"]))
            line = re.sub(pattern_multi, "", line).strip()

    pattern_random = re.compile(r"\[\s*(?P<word>randomx?)(?:\s+(?P<number>\d+))?\s*\]", re.IGNORECASE)
    pattern_number = re.compile(r"\[\s*(?P<word>number)(?:\s+(?P<number1>-?\d+)(?:\s+(?P<number2>-?\d+))?)?\s*\]", re.IGNORECASE)
    pattern_count = re.compile(r"\[(?P<word>count)\]", re.IGNORECASE)
    pattern_date = re.compile(r"\[\s*(?P<word>date)(?:\s+(?P<format>.*))?\s*\]", re.IGNORECASE)

    for _ in range(multi):
        new_line = line
        new_line = re.sub(pattern_random, replace_random, new_line)
        new_line = re.sub(pattern_number, replace_number, new_line)
        new_line = re.sub(pattern_count, replace_count, new_line)
        new_line = re.sub(pattern_date, replace_date, new_line)
        new_lines.append(new_line)

    return new_lines


def check_repeat() -> None:
    if not config.words:
        return

    new_lines: List[str] = []
    pattern = re.compile(
        r"^\[\s*(?P<word>rep(?:eat)?)\s*(?P<number>\d+)?\s*\]$", re.IGNORECASE)

    for line in config.words:
        match = re.match(pattern, line)

        if match:
            num = match["number"]
            number = int(num) if num is not None else 1
            new_lines.extend([new_lines[-1]] * number)
        else:
            new_lines.append(line)

    config.words = new_lines


def check_empty() -> None:
    if not config.words:
        return

    new_lines: List[str] = []
    pattern = re.compile(
        r"^\[\s*(?P<word>empty)(?:\s+(?P<number>\d+))?\s*\]$", re.IGNORECASE)

    for line in config.words:
        match = re.match(pattern, line)

        if match:
            num = match["number"]
            number = int(num) if num is not None else 1

            for _ in range(number):
                new_lines.append("")
        else:
            new_lines.append(line)

    config.words = new_lines


def random_word() -> str:
    if not config.randomlist:
        lines = config.randomfile.read_text().splitlines()
        config.randomlist = [line.strip() for line in lines]

    if not config.randwords:
        config.randwords = config.randomlist.copy()

    if not config.randwords:
        return ""

    w = config.random_words.choice(config.randwords)

    if not config.repeatrandom:
        config.randwords.remove(w)

    return w


def get_random(rand: str, allow_zero: bool) -> str:
    if rand == "random":
        return random_word().lower()
    elif rand == "RANDOM":
        return random_word().upper()
    elif rand == "Random":
        return random_word().capitalize()
    elif rand == "RanDom":
        return random_word().title()
    elif rand == "randomx":
        return random_word()
    elif rand == "number":
        return str(utils.random_digit(allow_zero))
    else:
        return ""
