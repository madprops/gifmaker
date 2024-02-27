# Modules
from configuration import config
import utils
import words

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

    frames = []
    path = config.get("input")
    ext = utils.get_extension(path)

    if (ext == "jpg") or (ext == "png"):
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

    num_frames = max_frames if config.get("remake") else config.get("frames")
    order = "normal" if (config.get("remake") or config.get("framelist")) else config.get("order")
    framelist = config.get("framelist") if config.get("framelist") else range(max_frames)
    current = 0

    # Sometimes it fails to read the frames so it needs more tries
    for _ in range(0, num_frames * 25):
        if order == "normal":
            index = framelist[current]
        elif order == "random":
            if config.get("frameopts"):
                index = random.choice(config.get("frameopts"))
            else:
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
    fontcolor = config.get_color("fontcolor")
    padding = config.get("padding")

    min_x = data["min_x"]
    min_y = data["min_y"]
    max_x = data["max_x"]
    max_y = data["max_y"]

    min_x_p = min_x - padding
    min_y_p = min_y - padding + data["ascender"]
    max_x_p = max_x + padding
    max_y_p = max_y + padding

    if not config.get("descender"):
        max_y_p -= data["descender"]

    if config.get("bgcolor"):
        bgcolor = config.get_color("bgcolor")
        alpha = utils.add_alpha(bgcolor, config.get("opacity"))
        rect_pos = (min_x_p, min_y_p), (max_x_p, max_y_p)
        draw.rounded_rectangle(rect_pos, fill=alpha, radius=config.get("radius"))

    if config.get("outline"):
        ocolor = config.get_color("outline")
        owidth = config.get("outlinewidth")
        owidth = utils.divisible(owidth, 2)
        halfwidth = owidth / 2

        if not config.get("no_outline_top"):
            draw.line([(min_x_p, min_y_p - halfwidth),
                       (max_x_p, min_y_p - halfwidth)], fill=ocolor, width=owidth)

        if not config.get("no_outline_left"):
            draw.line([(min_x_p - halfwidth, min_y_p - owidth + 1),
                       (min_x_p - halfwidth, max_y_p + owidth)], fill=ocolor, width=owidth)

        if not config.get("no_outline_bottom"):
            draw.line([(min_x_p, max_y_p + halfwidth),
                       (max_x_p, max_y_p + halfwidth)], fill=ocolor, width=owidth)

        if not config.get("no_outline_right"):
            draw.line([(max_x_p + halfwidth, min_y_p - owidth + 1),
                       (max_x_p + halfwidth, max_y_p + owidth)], fill=ocolor, width=owidth)

    draw.multiline_text((min_x, min_y), line, fill=fontcolor, font=font, align=config.get("align"))

    return frame


def get_text_data(frame: Image.Image, line: str, font: ImageFont.FreeTypeFont) -> Dict[str, int]:
    draw = ImageDraw.Draw(frame)
    width, height = frame.size

    p_top = config.get("top")
    p_bottom = config.get("bottom")
    p_left = config.get("left")
    p_right = config.get("right")

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
        if not config.get("descender"):
            text_y = height - b_bottom + descender - p_bottom
        else:
            text_y = height - b_bottom - p_bottom
    else:
        # Center Vertical
        if not config.get("descender"):
            text_y = (height - b_bottom + descender - ascender - (config.get("padding") / 2)) // 2
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
    if not config.get("words"):
        return frames

    worded = []
    num_words = len(config.get("words"))

    for i, frame in enumerate(frames):
        if config.get("fillgen"):
            line = words.generate(config.get("words")[0], False)[0]
        else:
            index = i

            if index >= num_words:
                if config.get("fillwords"):
                    index = num_words - 1
                else:
                    worded.append(frame)
                    continue

            line = config.get("words")[index]

        if line:
            frame = draw_text(frame, line)

        worded.append(frame)

    return worded


def resize_frames(frames: List[Image.Image]) -> List[Image.Image]:
    if (not config.get("width")) and (not config.get("height")):
        return frames

    new_frames = []
    new_width = config.get("width")
    new_height = config.get("height")
    w, h = frames[0].size
    ratio = w / h

    if new_width and (not new_height):
        new_height = int(new_width / ratio)
    elif new_height and (not new_width):
        new_width = int(new_height * ratio)

    if (new_width <= 0) or (new_height <= 0):
        return frames

    if config.get("nogrow"):
        if (new_width > w) or (new_height > h):
            return frames

    size = (new_width, new_height)

    for frame in frames:
        new_frames.append(frame.resize(size))

    return new_frames


def render(frames: List[Image.Image]) -> Union[Path, None]:
    ext = utils.get_extension(config.get("output"))
    fmt = ext if ext else config.get("format")

    if config.get("vertical") or config.get("horizontal"):
        if fmt not in ["jpg", "png"]:
            fmt = "png"

    def makedir(path: Path) -> None:
        try:
            path.mkdir(parents=False, exist_ok=True)
        except:
            utils.exit("Failed to make output directory")
            return

    if ext:
        makedir(config.get("output.parent"))
        output = config.get("output")
    else:
        makedir(config.get("output"))
        rand = utils.random_string()
        formt = config.get("format")
        file_name = f"{rand}.{formt}"
        output = Path(config.get("output"), file_name)

    if config.get("vertical"):
        frames = [append_frames(frames, "vertical")]

    if config.get("horizontal"):
        frames = [append_frames(frames, "horizontal")]

    if fmt == "gif":
        frames = to_array_all(frames)
        loop = None if config.get("loop") <= -1 else config.get("loop")
        imageio.mimsave(output, frames, format="GIF", duration=config.get("delay"), loop=loop)
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
        fps = 1000 / config.get("delay")

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
    if (config.get("filter") == "none") and (not config.get("filterlist")):
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

        if config.get("filteropts"):
            filters = config.get("filteropts").copy()
        elif config.get("filter").startswith("anyhue"):
            filters = hue_filters.copy()
        else:
            filters = all_filters.copy()

    def random_filter() -> str:
        filtr = config.Internal.random_filters.choice(filters)

        if not config.get("repeatfilter"):
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
    filtr = config.get("filter")

    if not config.get("filterlist"):
        if config.get("filter") == "random" or config.get("filter") == "anyhue":
            filtr = random_filter()

    for frame in frames:
        if config.get("filterlist"):
            filtr = config.get("filterlist").pop(0)
        elif config.get("filter") == "random2" or config.get("filter") == "anyhue2":
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
    if config.get("frames") is not None:
        return

    if config.get("framelist"):
        config.set("frames", len(config.get("framelist")))
    elif config.get("words"):
        num_words = len(config.get("words"))
        config.set("frames", num_words if num_words > 0 else config.get("frames"))
    else:
        config.set("frames", 3)


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
    if not config.get("deepfry"):
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
