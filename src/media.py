# Modules
from configuration import config
import utils

# Libraries
import imageio # type: ignore
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont # type: ignore

# Standard
import random
import colorsys
import numpy as np # type: ignore
from pathlib import Path
from typing import List, Any, Dict, Union, Tuple

def get_frames() -> List[Any]:
	count_frames()
	assert isinstance(config.frames, int)

	frames = []
	path = random.choice(config.input)
	ext = utils.get_extension(path)

	if ext == "jpg" or ext == "png":
		for _ in range(0, config.frames):
			img = to_pillow(imageio.imread(path), "RGB")
			frames.append(img)
	else:
		reader = imageio.get_reader(path)
		num_frames = len(reader) if config.remake else config.frames
		order = "normal" if (config.remake or config.framelist) else config.order
		framelist = config.framelist if config.framelist else range(reader.count_frames())
		current = 0

		# Sometimes it fails to read the frames so it needs more tries
		for _ in range(0, num_frames * 25):
			if order == "normal":
				index = framelist[current]
			elif order == "random":
				index = random.choice(framelist)

			try:
				img = to_pillow(reader.get_data(index), "RGB")
				frame = frames.append(img)
			except:
				pass

			if len(frames) == num_frames:
				break

			if order == "normal":
				current += 1

				if current >= len(framelist):
					current = 0

		reader.close()

	return frames

def add_text(frame: Any, line: str) -> Any:
	draw = ImageDraw.Draw(frame)
	font = get_font()
	data = get_text_data(frame, line)
	fontcolor = get_color(config.fontcolor)
	padding = config.padding

	if config.bgcolor:
		if config.baseline:
			baseline = data["framedata"][0]["baseline"]
		else:
			baseline = 0

		bgcolor = get_color(config.bgcolor)
		bgcolor = add_alpha(bgcolor, config.opacity)
		print(bgcolor)

		rect_1 = (data["min_x_rect"] - padding, data["min_y_rect"] - padding)
		rect_2 = (data["max_x_rect"] + padding, data["max_y_rect"] + padding + baseline)

		draw.rectangle([rect_1, rect_2], fill=bgcolor)

	position = (data["min_x_rect"], data["min_y_rect"])
	draw.text(position, line, fill=fontcolor, font=font)

	return frame

def get_font_item(name: str) -> Any:
	path = Path(config.fontspath, name)
	return ImageFont.truetype(path, size=config.fontsize)

def get_font() -> Any:
	font = get_font_item("Roboto-Regular.ttf")
	return font

def get_text_data(frame: Any, line: str) -> Dict[str, Any]:
	draw = ImageDraw.Draw(frame)
	width, height = get_shape(frame)
	font = get_font()
	framedata = []

	p_top = config.top
	p_bottom = config.bottom
	p_left = config.left
	p_right = config.right
	padding = config.padding

	text_size = draw.textbbox((0, 0), line, font)
	text_width = text_size[2]
	text_height = text_size[3]

	if (p_left is not None) and (p_left >= 0):
		text_x = p_left + padding
	elif (p_right is not None) and (p_right >= 0):
		text_x = width - text_width - p_right - padding
	else:
		text_x = (width - text_width) // 2

		if (p_left is not None) and (p_left < 0):
			text_x += p_left
		elif (p_right is not None) and (p_right < 0):
			text_x -= p_right

	if (p_top is not None) and (p_top >= 0):
		text_y = p_top + padding
	elif (p_bottom is not None) and (p_bottom >= 0):
		text_y = height - p_bottom - padding + text_height

		if config.baseline:
			text_y -= baseline
	else:
		text_y = (height - text_height) // 2

		if (p_top is not None) and (p_top < 0):
			text_y += p_top
		elif (p_bottom is not None) and (p_bottom < 0):
			text_y -= p_bottom

	ans = {
		"min_x_rect": text_x,
		"min_y_rect": text_y,
		"max_x_rect": text_x + text_width,
		"max_y_rect": text_y + text_height,
	}

	return ans

def word_frames(frames: List[Any]) -> List[Any]:
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
			frame = add_text(frame, line)

		worded.append(frame)

	return worded

def resize_frames(frames: List[Any]) -> List[Any]:
	if (not config.width) and (not config.height):
		return frames

	new_frames = []
	new_width = config.width
	new_height = config.height
	w, h = get_shape(frames[0])
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

def render(frames: List[Any]) -> Union[Path, None]:
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
		loop =  None if config.loop <= -1 else config.loop
		imageio.mimsave(output, frames, format="GIF", duration=config.delay, loop=loop)
	elif fmt == "png":
		imageio.imsave(output, frames[0], format="PNG")
	elif fmt == "jpg":
		imageio.imsave(output, frames[0], format="JPG")
	elif fmt == "mp4" or fmt == "webm":
		fps = 1000 / config.delay
		writer = imageio.get_writer(output, fps=fps)

		for frame in frames:
			writer.append_data(frame)

		writer.close()
	else:
		utils.exit("Invalid format")
		return None

	return output

def apply_filters(frames: List[Any]) -> List[Any]:
	if (config.filter == "none") and (not config.filterlist):
		return frames

	new_frames = []

	min_hue = 1
	max_hue = 8
	hue_step = 0.1

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

	def to_hsv(frame: Any) -> Any:
		return rgb_to_hsv(np.array(frame))

	def to_rgb(frame: Any) -> Any:
		return to_pillow(hsv_to_rgb(frame), "RGB")

	def change_hue(frame: Any, factor: float) -> Any:
		hsv_image = frame.convert("HSV")
		h, s, v = hsv_image.split()
		h = h.point(lambda i: i * factor)
		new_image = Image.merge("HSV", (h, s, v))
		return new_image.convert("RGB")

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
					new_frame = change_hue(frame, hue_step * n)
					break

		if new_frame is None:
			if filtr == "gray":
				new_frame = frame.convert("L")
			elif filtr == "blur":
				new_frame = frame.filter(ImageFilter.BLUR)
			elif filtr == "invert":
				new_frame = ImageOps.invert(frame)
			else:
				new_frame = frame

		new_frames.append(new_frame)

	return new_frames

def get_shape(frame: Any) -> Tuple[int, int]:
	return frame.size

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

def get_color(value: Union[str, List[int]]) -> List[int]:
	rgb = None

	if isinstance(value, str):
		if value == "light2":
			rgb = utils.random_light()
		elif value == "dark2":
			rgb = utils.random_dark()
	elif isinstance(value, list):
		rgb = value

	return tuple(rgb) or (100, 100, 100)

def add_alpha(rgb: Tuple[int, int, int], alpha: float) -> Tuple[int, int, int, int]:
	return int(rgb[0]), int(rgb[1]), int(rgb[2]), int(255 * alpha)

def to_pillow(frame: Any, mode: str) -> Any:
	return Image.fromarray(frame, mode=mode)

def to_array(frames: Any) -> Any:
	return [np.array(frame) for frame in frames]