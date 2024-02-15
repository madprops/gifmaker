# Modules
from args import Global
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
		for _ in range(0, Global.frames):
			frame = cv2.imread(str(path))
			frames.append(frame)
	else:
		cap = cv2.VideoCapture(str(path))
		total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		num_frames = total_frames if Global.remake else Global.frames
		order = "normal" if Global.remake else Global.order
		framelist = Global.framelist if Global.framelist else range(total_frames)
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

def add_text(frame, text, lineheight):
	if not text:
		return frame, 0

	width, height = get_shape(frame)

	if Global.font == "simple":
		font = cv2.FONT_HERSHEY_SIMPLEX
	elif Global.font == "complex":
		font = cv2.FONT_HERSHEY_COMPLEX
	elif Global.font == "plain":
		font = cv2.FONT_HERSHEY_PLAIN
	elif Global.font == "duplex":
		font = cv2.FONT_HERSHEY_DUPLEX
	elif Global.font == "triplex":
		font = cv2.FONT_HERSHEY_TRIPLEX

	text_size, baseline = cv2.getTextSize(text, font, Global.fontsize, Global.boldness)

	text_width = text_size[0]
	text_height = text_size[1]

	p_top = Global.top
	p_bottom = Global.bottom
	p_left = Global.left
	p_right = Global.right

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
	text_position = (text_x, text_y)
	rgb = list(reversed((Global.fontcolor)))

	if Global.bgcolor:
		if Global.baseline:
			bline = baseline
		else:
			bline = 0

		padding = Global.padding
		rect_x = text_x - padding
		rect_y = text_y - text_height - padding
		rect_width = padding + text_width + padding
		rect_height = padding + text_height + bline + padding
		rect_1 = (rect_x, rect_y)
		rect_2 = (rect_x + rect_width, rect_y + rect_height)
		rcopy = cv2.rectangle(frame.copy(), rect_1, rect_2, Global.bgcolor, -1)
		cv2.addWeighted(frame, 1 - Global.opacity, rcopy, Global.opacity, 0, frame)

	cv2.putText(frame, text, text_position, font, Global.fontsize, rgb, Global.boldness, cv2.LINE_AA)
	return frame, text_height

def word_frames(frames):
	if not Global.words:
		return frames

	worded = []
	num_words = len(Global.words)

	for i, frame in enumerate(frames):
		if i >= num_words:
			worded.append(frame)
			continue

		lines = [line.strip() for line in Global.words[i].split(Global.linebreak)]
		lineheight = 0

		for line in lines:
			frame, height = add_text(frame, line, lineheight)
			lineheight += height + Global.linespace

		worded.append(frame)

	return worded

def resize_frames(frames):
	if Global.width is None:
		return frames

	new_frames = []

	for frame in frames:
		w, h = get_shape(frame)
		ratio = w / h
		height = int(Global.width / ratio)
		new_frames.append(cv2.resize(frame, (Global.width, height)))

	return new_frames

def render(frames):
	ext = utils.get_extension(Global.output)
	err_msg = "Failed to make output directory"

	if ext:
		try:
			Global.output.parent.mkdir(parents=False, exist_ok=True)
		except:
			utils.exit(err_msg)

		output = Global.output
	else:
		try:
			Global.output.mkdir(parents=False, exist_ok=True)
		except:
			utils.exit(err_msg)

		rand = utils.random_string()
		file_name = f"{rand}.{Global.format}"
		output = Path(Global.output, file_name)

	fmt = ext if ext else Global.format

	if fmt == "gif":
		loop =  None if Global.loop <= -1 else Global.loop
		frames = to_pillow(frames)
		frames[0].save(output, save_all=True, append_images=frames[1:], duration=Global.delay, loop=loop, optimize=True)
	elif fmt == "mp4":
		width, height = get_shape(frames[0])
		fourcc = cv2.VideoWriter_fourcc(*"mp4v")
		fps = 1000 / Global.delay
		out = cv2.VideoWriter(str(output), fourcc, fps, (width, height))

		for frame in frames:
			out.write(frame)

		out.release()

	print(f"\nSaved as: {output}\n")

def to_pillow(frames):
	new_frames = []

	for frame in frames:
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(rgb_frame)
		new_frames.append(pil_image)

	return new_frames

def apply_filters(frames):
	if (not Global.filter) and (not Global.filterlist):
		return frames

	new_frames = []
	hue_step = 20

	def get_hsv(frame):
		return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	def do_hsv(hsv):
		return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

	filters = ["hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8",
	"gray", "blur", "invert", "saturate"]

	filter = Global.filter

	if not Global.filterlist:
		if Global.filter == "random":
			filter = random.choice(filters)

	for frame in frames:
		if Global.filterlist:
			filter = Global.filterlist.pop(0)
		elif Global.filter == "random2":
			filter = random.choice(filters)

		for n in range(1, 9):
			if filter == f"hue{n}":
				hsv = get_hsv(frame)
				hsv[:, :, 0] = (hsv[:, :, 0] + hue_step * n) % 180
				new_frame = do_hsv(hsv)
				break

		if filter == "gray":
			new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			new_frame = cv2.cvtColor(new_frame, cv2.COLOR_GRAY2BGR)
		elif filter == "blur":
			new_frame = cv2.GaussianBlur(frame, (45, 45), 0)
		elif filter == "invert":
			new_frame = cv2.bitwise_not(frame)
		elif filter == "saturate":
			hsv = get_hsv(frame)
			hsv[:, :, 0] = 0
			hsv[:, :, 2] = 255
			new_frame = do_hsv(hsv)

		new_frames.append(new_frame)

	return new_frames

def get_shape(frame):
	return frame.shape[1], frame.shape[0]

def count_frames():
	if Global.framelist:
		Global.frames = len(Global.framelist)
	else:
		num_words = len(Global.words)
		Global.frames = num_words if num_words > 0 else Global.frames