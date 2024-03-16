# Modules
from .config import config
from . import utils
from . import words

# Libraries
import imageio  # type: ignore
import numpy as np
import numpy.typing as npt
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont  # type: ignore

# Standard
import random
from io import BytesIO
from pathlib import Path
from typing import List, Dict, Union


def get_frames() -> List[Image.Image]:
    count_frames()

    assert isinstance(config.frames, int)
    assert isinstance(config.input, Path)

    frames = []
    path = config.input
    ext = utils.get_extension(path)

    if (ext == "jpg") or (ext == "jpeg") or (ext == "png"):
        reader = imageio.imread(path)
        max_frames = 1
        mode = "image"
    elif ext == "gif":
        reader = imageio.mimread(path)
        max_frames = len(reader)
        mode = "gif"
    else:
        reader = imageio.get_reader(path)
        max_frames = reader.count_frames()
        mode = "video"

    num_frames = max_frames if config.remake else config.frames
    order = "normal" if (config.remake or config.framelist) else config.order
    framelist = config.framelist if config.framelist else range(max_frames)
    current = 0

    # Sometimes it fails to read the frames so it needs more tries
    for _ in range(0, num_frames * 25):
        if order == "normal":
            index = framelist[current]
        elif order == "random":
            if config.frameopts:
                index = random.choice(config.frameopts)
            else:
                assert isinstance(config.Internal.random_frames, random.Random)
                index = config.Internal.random_frames.randint(0, len(framelist))

        try:
            if mode == "image":
                img = reader
            elif mode == "video":
                img = reader.get_data(index)
            elif mode == "gif":
                img = reader[index]

            frames.append(to_pillow(img))
        except Exception as e:
            pass

        if len(frames) == num_frames:
            break

        if order == "normal":
            current += 1

            if current >= len(framelist):
                current = 0

    if mode == "video":
        reader.close()

    return frames


def draw_text(frame: Image.Image, line: str) -> Image.Image:
    draw = ImageDraw.Draw(frame, "RGBA")
    font = config.get_font()
    data = get_text_data(frame, line, font)
    get_colors = True

    if line == config.Internal.last_words:
        if config.word_color_mode == "normal":
            get_colors = False

    if not config.Internal.last_colors:
        get_colors = True

    if get_colors:
        fontcolor = config.get_color("fontcolor")
        bgcolor = config.get_color("bgcolor")
        ocolor = config.get_color("outline")
    else:
        fontcolor = config.Internal.last_colors[0]
        bgcolor = config.Internal.last_colors[1]
        ocolor = config.Internal.last_colors[2]

    config.Internal.last_colors = [fontcolor, bgcolor, ocolor]
    config.Internal.last_words = line

    min_x = data["min_x"]
    min_y = data["min_y"]
    max_x = data["max_x"]
    max_y = data["max_y"]

    min_x_p = min_x - config.padding
    min_y_p = min_y - config.padding + data["ascender"]
    max_x_p = max_x + config.padding
    max_y_p = max_y + config.padding

    if not config.descender:
        max_y_p -= data["descender"]

    if config.bgcolor:
        alpha = utils.add_alpha(bgcolor, config.opacity)
        rect_pos = (min_x_p, min_y_p), (max_x_p, max_y_p)
        draw.rounded_rectangle(rect_pos, fill=alpha, radius=config.radius)

    if config.outline:
        owidth = config.outlinewidth
        owidth = utils.divisible(owidth, 2)
        halfwidth = owidth / 2

        if not config.no_outline_top:
            draw.line([(min_x_p, min_y_p - halfwidth),
                       (max_x_p, min_y_p - halfwidth)], fill=ocolor, width=owidth)

        if not config.no_outline_left:
            draw.line([(min_x_p - halfwidth, min_y_p - owidth + 1),
                       (min_x_p - halfwidth, max_y_p + owidth)], fill=ocolor, width=owidth)

        if not config.no_outline_bottom:
            draw.line([(min_x_p, max_y_p + halfwidth),
                       (max_x_p, max_y_p + halfwidth)], fill=ocolor, width=owidth)

        if not config.no_outline_right:
            draw.line([(max_x_p + halfwidth, min_y_p - owidth + 1),
                       (max_x_p + halfwidth, max_y_p + owidth)], fill=ocolor, width=owidth)

    draw.multiline_text((min_x, min_y), line, fill=fontcolor, font=font, align=config.align)

    return frame


def get_text_data(frame: Image.Image, line: str, font: ImageFont.FreeTypeFont) -> Dict[str, int]:
    draw = ImageDraw.Draw(frame)
    width, height = frame.size

    p_top = config.top
    p_bottom = config.bottom
    p_left = config.left
    p_right = config.right

    b_left, b_top, b_right, b_bottom = draw.multiline_textbbox((0, 0), line, font=font)
    ascender = font.getbbox(line.split("\n")[0])[1]
    descender = font.getbbox(line.split("\n")[-1], anchor="ls")[3]

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
        text_y = p_top - ascender
    # Bottom
    elif (p_bottom is not None) and (p_bottom >= 0):
        if not config.descender:
            text_y = height - b_bottom + descender - p_bottom
        else:
            text_y = height - b_bottom - p_bottom
    else:
        # Center Vertical
        if not config.descender:
            text_y = (height - b_bottom + descender - ascender - (config.padding / 2)) // 2
        else:
            text_y = (height - b_bottom - ascender) // 2

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
        "ascender": ascender,
        "descender": descender,
    }

    return ans


def word_frames(frames: List[Image.Image]) -> List[Image.Image]:
    if not config.words:
        return frames

    worded = []
    num_words = len(config.words)

    for i, frame in enumerate(frames):
        if config.fillgen:
            line = words.generate(config.words[0], False)[0]
        else:
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
    assert isinstance(config.output, Path)
    ext = utils.get_extension(config.output)
    fmt = ext if ext else config.format

    if config.vertical or config.horizontal:
        if fmt not in ["jpg", "png"]:
            fmt = "png"

    def makedir(path: Path) -> None:
        try:
            path.mkdir(parents=False, exist_ok=True)
        except BaseException:
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

    if config.vertical:
        frames = [append_frames(frames, "vertical")]

    if config.horizontal:
        frames = [append_frames(frames, "horizontal")]

    if fmt == "gif":
        frames = to_array_all(frames)
        loop = None if config.loop <= -1 else config.loop
        imageio.mimsave(output, frames, format="GIF", duration=config.delay, loop=loop)
    elif fmt == "png":
        frame = frames[0]
        frame = to_array(frame)
        imageio.imsave(output, frame, format="PNG")
    elif fmt == "jpg":
        frame = frames[0]
        frame = frame.convert("RGB")
        frame = to_array(frame)
        imageio.imsave(output, frame, format="JPEG")
    elif fmt == "mp4" or fmt == "webm":
        frames = to_array_all(frames)
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
        assert isinstance(config.Internal.random_filters, random.Random)
        filtr = config.Internal.random_filters.choice(filters)

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

        if frame.mode in ["RGBA", "LA"]:
            new_frame = Image.merge("RGBA", (new_frame.split() + (frame.split()[3],)))
        else:
            new_frame = new_frame.convert("RGB")

        return new_frame

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
            if filtr in ["gray", "grey"]:
                if frame.mode in ["RGBA", "LA"]:
                    r, g, b, a = frame.split()
                    gray_img = ImageOps.grayscale(frame.convert("RGB"))
                    rgb_gray = ImageOps.colorize(gray_img, "black", "white")
                    new_frame = Image.merge("RGBA", (rgb_gray.split() + (a,)))
                else:
                    new_frame = ImageOps.colorize(frame.convert("L"), "black", "white")
            elif filtr == "blur":
                new_frame = frame.filter(ImageFilter.BLUR)
            elif filtr == "invert":
                new_frame = ImageOps.invert(frame.convert("RGB"))
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


def rgb_or_rgba(array: npt.NDArray[np.float64]) -> str:
    if array.shape[2] == 4:
        return "RGBA"
    else:
        return "RGB"


def to_pillow(array: npt.NDArray[np.float64]) -> Image.Image:
    mode = rgb_or_rgba(array)
    return Image.fromarray(array, mode=mode)


def to_array(frame: Image.Image) -> npt.NDArray[np.float64]:
    return np.array(frame)


def to_array_all(frames: List[Image.Image]) -> List[npt.NDArray[np.float64]]:
    return [to_array(frame) for frame in frames]


def deep_fry(frames: List[Image.Image]) -> List[Image.Image]:
    if not config.deepfry:
        return frames

    quality = 3
    new_frames = []

    for frame in frames:
        stream = BytesIO()
        frame = frame.convert("RGB")
        frame.save(stream, format="JPEG", quality=quality)
        new_frames.append(Image.open(stream))

    return new_frames


def append_frames(frames: List[Image.Image], mode: str) -> Image.Image:
    widths, heights = zip(*(i.size for i in frames))

    if mode == "vertical":
        total_width = max(widths)
        total_height = sum(heights)
    elif mode == "horizontal":
        total_width = sum(widths)
        total_height = max(heights)

    new_frame = Image.new("RGB", (total_width, total_height))
    offset = 0

    for frame in frames:
        if mode == "vertical":
            new_frame.paste(frame, (0, offset))
            offset += frame.size[1]
        elif mode == "horizontal":
            new_frame.paste(frame, (offset, 0))
            offset += frame.size[0]

    return new_frame
