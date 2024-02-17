# Modules
from configuration import config
import utils

# Libraries
import cv2
from PIL import Image

# Standard
from pathlib import Path
import random

def get_frames(path):
	frames = []
	ext = utils.get_extension(path)

	if ext == ".jpg" or ext == ".png":
		for _ in range(0, config.frames):
			frame = cv2.imread(str(path))
			frames.append(frame)
	else:
		cap = cv2.VideoCapture(str(path))
		total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		num_frames = total_frames if config.remake else config.frames
		order = "normal" if config.remake else config.order
		framelist = config.framelist if config.framelist else range(total_frames)
		current = 0

		# Sometimes it fails to read the frames so it needs more tries
		for _ in range(0, num_frames * 25):
			if order == "normal":
				index = framelist[current]
			elif order == "random":
				index = random.choice(framelist)

			cap.set(cv2.CAP_PROP_POS_FRAMES, index)
			ret, frame = cap.read()

			if ret:
				frames.append(frame)

			if len(frames) == num_frames:
				break

			if order == "normal":
				current += 1

				if current >= len(framelist):
					current = 0

		cap.release()

	return frames

def add_text(frame, lines):
	font = get_font()
	data = get_text_data(frame, lines)
	rgb_font = list(reversed((config.fontcolor)))
	padding = config.padding

	if config.bgcolor:
		if config.baseline:
			baseline = data["framedata"][0]["baseline"]
		else:
			baseline = 0

		rgb_bg = list(reversed((config.bgcolor)))
		rect_1 = (data["min_x_rect"] - padding, data["min_y_rect"] - padding)
		rect_2 = (data["max_x_rect"] + padding, data["max_y_rect"] + padding + baseline)

		cv2.rectangle(frame, (rect_1), rect_2, rgb_bg, -1)

	for i, line in enumerate(lines):
		framedata = data["framedata"][i]
		position = (framedata["x"], framedata["y"])
		cv2.putText(frame, line, position, font, config.fontsize, rgb_font, config.boldness, cv2.LINE_AA)

	return frame

def get_font():
	if config.font == "simple":
		font = cv2.FONT_HERSHEY_SIMPLEX
	elif config.font == "complex":
		font = cv2.FONT_HERSHEY_COMPLEX
	elif config.font == "plain":
		font = cv2.FONT_HERSHEY_PLAIN
	elif config.font == "duplex":
		font = cv2.FONT_HERSHEY_DUPLEX
	elif config.font == "triplex":
		font = cv2.FONT_HERSHEY_TRIPLEX

	return font

def get_text_data(frame, lines):
	width, height = get_shape(frame)
	max_width, max_height = 0, 0
	font = get_font()
	lineheight = 0
	framedata = []

	for line in lines:
		text_size, baseline = cv2.getTextSize(line, font, config.fontsize, config.boldness)
		text_width = text_size[0]
		text_height = text_size[1]
		max_height += text_height + config.linespace

		if text_width > max_width:
			max_width = text_width

		p_top = config.top
		p_bottom = config.bottom
		p_left = config.left
		p_right = config.right

		if (p_left is not None) and (p_left >= 0):
			text_x = p_left
		elif (p_right is not None) and (p_right >= 0):
			text_x = width - text_width - p_right
		else:
			text_x = (width - text_width) // 2

			if (p_left is not None) and (p_left < 0):
				text_x += p_left
			elif (p_right is not None) and (p_right < 0):
				text_x -= p_right

		if (p_top is not None) and (p_top >= 0):
			text_y = text_height + p_top
		elif (p_bottom is not None) and (p_bottom >= 0):
			text_y = height - baseline - p_bottom
		else:
			text_y = (height + text_height) // 2

			if (p_top is not None) and (p_top < 0):
				text_y += p_top
			elif (p_bottom is not None) and (p_bottom < 0):
				text_y -= p_bottom

		text_y += lineheight
		lineheight += text_height + config.linespace
		x_rect = text_x
		y_rect = text_y - text_height

		fdata = {
			"width": text_width,
			"height": text_height,
			"x": text_x,
			"y": text_y,
			"x_rect": x_rect,
			"y_rect": y_rect,
			"baseline": baseline,
		}

		framedata.append(fdata)

	min_x, min_y, min_x_rect, min_y_rect = float("inf"), float("inf"), float("inf"), float("inf")
	max_x, max_y, max_x_rect, max_y_rect = 0, 0, 0, 0

	for item in framedata:
		min_x = min(min_x, item["x"])
		min_y = min(min_y, item["y"])
		max_x = max(max_x, item["x"] + item["width"])
		max_y = max(max_y, item["y"] + item["height"])
		min_x_rect = min(min_x_rect, item["x_rect"])
		min_y_rect = min(min_y_rect, item["y_rect"])
		max_x_rect = max(max_x_rect, item["x_rect"] + item["width"])
		max_y_rect = max(max_y_rect, item["y_rect"] + item["height"])

	ans = {
		"width": width,
		"height": height,
		"framedata": framedata,
		"max_width": max_width,
		"max_height": max_height,
		"max_x": max_x,
		"max_y": max_y,
		"min_x": min_x,
		"min_y": min_y,
		"max_x_rect": max_x_rect,
		"max_y_rect": max_y_rect,
		"min_x_rect": min_x_rect,
		"min_y_rect": min_y_rect,
	}

	return ans

def word_frames(frames):
	if not config.words:
		return frames

	worded = []
	num_words = len(config.words)

	for i, frame in enumerate(frames):
		if i >= num_words:
			worded.append(frame)
			continue

		lines = [line.strip() for line in config.words[i].split(config.linebreak)]

		if any(element.strip() for element in lines):
			frame = add_text(frame, lines)

		worded.append(frame)

	return worded

def resize_frames(frames):
	if config.width is None:
		return frames

	new_frames = []

	for frame in frames:
		w, h = get_shape(frame)
		ratio = w / h
		height = int(config.width / ratio)
		new_frames.append(cv2.resize(frame, (config.width, height)))

	return new_frames

def render(frames):
	ext = utils.get_extension(config.output)
	err_msg = "Failed to make output directory"

	if ext:
		try:
			config.output.parent.mkdir(parents=False, exist_ok=True)
		except:
			utils.exit(err_msg)

		output = config.output
	else:
		try:
			config.output.mkdir(parents=False, exist_ok=True)
		except:
			utils.exit(err_msg)

		rand = utils.random_string()
		file_name = f"{rand}.{config.format}"
		output = Path(config.output, file_name)

	fmt = ext if ext else config.format

	if fmt == "gif":
		loop =  None if config.loop <= -1 else config.loop
		frames = to_pillow(frames)
		frames[0].save(output, save_all=True, append_images=frames[1:], duration=config.delay, loop=loop, optimize=True)
	elif fmt == "mp4":
		width, height = get_shape(frames[0])
		fourcc = cv2.VideoWriter_fourcc(*"mp4v")
		fps = 1000 / config.delay
		out = cv2.VideoWriter(str(output), fourcc, fps, (width, height))

		for frame in frames:
			out.write(frame)

		out.release()

	return output

def to_pillow(frames):
	new_frames = []

	for frame in frames:
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(rgb_frame)
		new_frames.append(pil_image)

	return new_frames

def apply_filters(frames):
	if (not config.filter) and (not config.filterlist):
		return frames

	new_frames = []
	hue_step = 20

	def get_hsv(frame):
		return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	def do_hsv(hsv):
		return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

	all_filters = ["hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8",
	"gray", "blur", "invert", "saturate", "none"]

	if config.filteropts:
		filters = config.filteropts
	else:
		filters = all_filters

	filtr = config.filter

	if not config.filterlist:
		if config.filter == "random":
			filtr = random.choice(filters)

	for frame in frames:
		if config.filterlist:
			filtr = config.filterlist.pop(0)
		elif config.filter == "random2":
			filtr = random.choice(filters)

		new_frame = None

		for n in range(1, 9):
			if filtr == f"hue{n}":
				hsv = get_hsv(frame)
				hsv[:, :, 0] = (hsv[:, :, 0] + hue_step * n) % 180
				new_frame = do_hsv(hsv)
				break

		if new_frame is None:
			if filtr == "gray":
				new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				new_frame = cv2.cvtColor(new_frame, cv2.COLOR_GRAY2BGR)
			elif filtr == "blur":
				new_frame = cv2.GaussianBlur(frame, (45, 45), 0)
			elif filtr == "invert":
				new_frame = cv2.bitwise_not(frame)
			elif filtr == "saturate":
				hsv = get_hsv(frame)
				hsv[:, :, 0] = 0
				hsv[:, :, 2] = 255
				new_frame = do_hsv(hsv)
			else:
				new_frame = frame

		new_frames.append(new_frame)

	return new_frames

def get_shape(frame):
	return frame.shape[1], frame.shape[0]

def count_frames():
	if config.frames is not None:
		return

	if config.framelist:
		config.frames = len(config.framelist)
	elif config.words:
		num_words = len(config.words)
		config.frames = num_words if num_words > 0 else config.frames
	else:
		config.frames = 3