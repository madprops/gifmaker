# Modules
from configuration import config
import utils

# Libraries
import imageio  # type: ignore
import numpy as np
import numpy.typing as npt
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont  # type: ignore

# Standard
import random
from pathlib import Path
from typing import List, Dict, Union, Tuple


def get_frames() -> List[Image.Image]:
    count_frames()
    assert isinstance(config.frames, int)

    frames = []
    path = random.choice(config.input)
    ext = utils.get_extension(path)

    if ext == "jpg" or ext == "png":
        for _ in range(0, config.frames):
            img = to_pillow(imageio.imread(path), "RGB")
            frames.append(img)

            if one_frame():
                break
    else:
        if ext == "gif":
            reader = imageio.mimread(path)
            max_frames = len(reader)
            video = False
        else:
            reader = imageio.get_reader(path)
            max_frames = reader.count_frames()
            video = True

        num_frames = max_frames if config.remake else config.frames
        order = "normal" if (config.remake or config.framelist) else config.order
        framelist = config.framelist if config.framelist else range(max_frames)
        current = 0

        # Sometimes it fails to read the frames so it needs more tries
        for _ in range(0, num_frames * 25):
            if order == "normal":
                index = framelist[current]
            elif order == "random":
                index = random.randint(0, len(framelist))

            try:
                if video:
                    img = reader.get_data(index)
                else:
                    img = reader[index]

                frames.append(to_pillow(img, "RGB"))

                if one_frame():
                    break
            except:
                pass

            if len(frames) == num_frames:
                break

            if order == "normal":
                current += 1

                if current >= len(framelist):
                    current = 0

        if video:
            reader.close()

    return frames


def draw_text(frame: Image.Image, line: str) -> Image.Image:
    draw = ImageDraw.Draw(frame, "RGBA")
    font = get_font()
    data = get_text_data(frame, line, font)
    fontcolor = config.get_color("fontcolor")
    _, top, _, _ = font.getbbox(line)
    padding = config.padding

    min_x = data["min_x"]
    min_y = data["min_y"]
    max_x = data["max_x"]
    max_y = data["max_y"]

    min_x_p = min_x - padding
    min_y_p = min_y - padding + top
    max_x_p = max_x + padding
    max_y_p = max_y + padding

    if config.bgcolor:
        bgcolor = config.get_color("bgcolor")
        alpha = utils.add_alpha(bgcolor, config.opacity)
        rect_pos = (min_x_p, min_y_p), (max_x_p, max_y_p)
        draw.rounded_rectangle(rect_pos, fill=alpha, radius=config.radius)

    if config.outline:
        ocolor = config.get_color("outline")
        owidth = config.outlinewidth
        owidth = utils.divisible(owidth, 2)
        halfwidth = owidth / 2

        if not config.notopoutline:
            draw.line([(min_x_p, min_y_p - halfwidth),
                       (max_x_p, min_y_p - halfwidth)], fill=ocolor, width=owidth)

        if not config.noleftoutline:
            draw.line([(min_x_p - halfwidth, min_y_p - owidth + 1),
                       (min_x_p - halfwidth, max_y_p + owidth)], fill=ocolor, width=owidth)

        if not config.nobottomoutline:
            draw.line([(min_x_p, max_y_p + halfwidth),
                       (max_x_p, max_y_p + halfwidth)], fill=ocolor, width=owidth)

        if not config.norightoutline:
            draw.line([(max_x_p + halfwidth, min_y_p - owidth + 1),
                       (max_x_p + halfwidth, max_y_p + owidth)], fill=ocolor, width=owidth)

    draw.multiline_text((min_x, min_y), line, fill=fontcolor, font=font, align=config.align)

    return frame


def get_font_item(font_file: str) -> ImageFont.FreeTypeFont:
    path = Path(config.fontspath, font_file)
    return ImageFont.truetype(path, size=config.fontsize)


def get_font() -> ImageFont.FreeTypeFont:
    fonts = {
        "sans": "Roboto-Regular.ttf",
        "serif": "RobotoSerif-Regular.ttf",
        "mono": "RobotoMono-Regular.ttf",
        "italic": "Roboto-Italic.ttf",
        "bold": "Roboto-Bold.ttf",
        "cursive": "Pacifico-Regular.ttf",
        "comic": "ComicNeue-Regular.ttf",
    }

    def random_font() -> str:
        return random.choice(list(fonts.keys()))

    if config.font == "random":
        font = random_font()
        font_file = fonts[font]
        config.font = font
    elif config.font == "random2":
        font = random_font()
        font_file = fonts[font]
    else:
        font_file = fonts[config.font]

    return get_font_item(font_file)


def get_text_data(frame: Image.Image, line: str, font: ImageFont.FreeTypeFont) -> Dict[str, int]:
    draw = ImageDraw.Draw(frame)
    width, height = frame.size

    p_top = config.top
    p_bottom = config.bottom
    p_left = config.left
    p_right = config.right

    _, _, b_right, b_bottom = draw.textbbox((0, 0), line, font=font)

    # Left
    if (p_left is not None) and (p_left >= 0):
        text_x = p_left
    # Right
    elif (p_right is not None) and (p_right >= 0):
        text_x = width - b_right - p_right
    else:
        # Center Horizontal
        text_x = (width - b_right) // 2

        # Negatives Horizontal
        if (p_left is not None) and (p_left < 0):
            text_x += p_left
        elif (p_right is not None) and (p_right < 0):
            text_x -= p_right

    # Top
    if (p_top is not None) and (p_top >= 0):
        text_y = p_top
    # Bottom
    elif (p_bottom is not None) and (p_bottom >= 0):
        text_y = height - p_bottom - b_bottom
    else:
        # Center Vertical
        text_y = (height - b_bottom) // 2

        # Negatives Vertical
        if (p_top is not None) and (p_top < 0):
            text_y += p_top
        elif (p_bottom is not None) and (p_bottom < 0):
            text_y -= p_bottom

    ans = {
        "min_x": text_x,
        "min_y": text_y,
        "max_x": text_x + b_right,
        "max_y": text_y + b_bottom,
    }

    return ans


def word_frames(frames: List[Image.Image]) -> List[Image.Image]:
    if not config.words:
        return frames

    worded = []
    num_words = len(config.words)

    for i, frame in enumerate(frames):
        index = i

        if index >= num_words:
            if config.fillwords:
                index = num_words - 1
            else:
                worded.append(frame)
                continue

        line = config.words[index]

        if line:
            frame = draw_text(frame, line)

        worded.append(frame)

    return worded


def resize_frames(frames: List[Image.Image]) -> List[Image.Image]:
    if (not config.width) and (not config.height):
        return frames

    new_frames = []
    new_width = config.width
    new_height = config.height
    w, h = frames[0].size
    ratio = w / h

    if new_width and (not new_height):
        new_height = int(new_width / ratio)
    elif new_height and (not new_width):
        new_width = int(new_height * ratio)

    assert isinstance(new_width, int)
    assert isinstance(new_height, int)

    if (new_width <= 0) or (new_height <= 0):
        return frames

    if config.nogrow:
        if (new_width > w) or (new_height > h):
            return frames

    size = (new_width, new_height)

    for frame in frames:
        new_frames.append(frame.resize(size))

    return new_frames


def render(frames: List[Image.Image]) -> Union[Path, None]:
    ext = utils.get_extension(config.output)

    def makedir(path: Path) -> None:
        try:
            path.mkdir(parents=False, exist_ok=True)
        except:
            utils.exit("Failed to make output directory")
            return

    if ext:
        makedir(config.output.parent)
        output = config.output
    else:
        makedir(config.output)
        rand = utils.random_string()
        file_name = f"{rand}.{config.format}"
        output = Path(config.output, file_name)

    fmt = ext if ext else config.format
    frames = to_array(frames)

    if fmt == "gif":
        loop = None if config.loop <= -1 else config.loop
        imageio.mimsave(output, frames, format="GIF", duration=config.delay, loop=loop)
    elif fmt == "png":
        imageio.imsave(output, frames[0], format="PNG")
    elif fmt == "jpg":
        imageio.imsave(output, frames[0], format="JPG")
    elif fmt == "mp4" or fmt == "webm":
        fps = 1000 / config.delay

        if fmt == "mp4":
            codec = "libx264"
        elif fmt == "webm":
            codec = "libvpx"

        writer = imageio.get_writer(output, fps=fps, codec=codec)

        for frame in frames:
            writer.append_data(frame)

        writer.close()
    else:
        utils.exit("Invalid format")
        return None

    return output


def apply_filters(frames: List[Image.Image]) -> List[Image.Image]:
    if (config.filter == "none") and (not config.filterlist):
        return frames

    new_frames = []

    min_hue = 1
    max_hue = 8
    hue_step = 20

    hue_filters = [f"hue{i}" for i in range(min_hue, max_hue + 1)]
    all_filters = hue_filters + ["gray", "blur", "invert", "none"]
    filters = []

    def get_filters() -> None:
        nonlocal filters

        if config.filteropts:
            filters = config.filteropts.copy()
        elif config.filter.startswith("anyhue"):
            filters = hue_filters.copy()
        else:
            filters = all_filters.copy()

    def random_filter() -> str:
        filtr = random.choice(filters)

        if not config.repeatfilter:
            remove_filter(filtr)

        return filtr

    def remove_filter(filtr: str) -> None:
        if filtr in filters:
            filters.remove(filtr)

        if not filters:
            get_filters()

    def change_hue(frame: Image.Image, n: int) -> Image.Image:
        hsv = frame.convert("HSV")
        h, s, v = hsv.split()
        h = h.point(lambda i: (i + hue_step * n) % 180)
        new_frame = Image.merge("HSV", (h, s, v))
        return new_frame.convert("RGB")

    get_filters()
    filtr = config.filter

    if not config.filterlist:
        if config.filter == "random" or config.filter == "anyhue":
            filtr = random_filter()

    for frame in frames:
        if config.filterlist:
            filtr = config.filterlist.pop(0)
        elif config.filter == "random2" or config.filter == "anyhue2":
            filtr = random_filter()

        new_frame = None

        if filtr.startswith("hue"):
            for n in range(min_hue, max_hue + 1):
                if filtr == f"hue{n}":
                    new_frame = change_hue(frame, n)
                    break

        if new_frame is None:
            if filtr == "gray":
                new_frame = ImageOps.colorize(frame.convert("L"), "black", "white")
            elif filtr == "blur":
                new_frame = frame.filter(ImageFilter.BLUR)
            elif filtr == "invert":
                new_frame = ImageOps.invert(frame)
            else:
                new_frame = frame

        new_frames.append(new_frame)

    return new_frames


def count_frames() -> None:
    if config.frames is not None:
        return

    if config.framelist:
        config.frames = len(config.framelist)
    elif config.words:
        num_words = len(config.words)
        config.frames = num_words if num_words > 0 else config.frames
    else:
        config.frames = 3


def to_pillow(frame: npt.NDArray[np.float64], mode: str) -> Image.Image:
    return Image.fromarray(frame, mode=mode)


def to_array(frames: List[Image.Image]) -> List[npt.NDArray[np.float64]]:
    return [np.array(frame) for frame in frames]


def one_frame() -> bool:
    return config.format.lower() in ["jpg", "png"]
