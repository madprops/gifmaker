# Modules
from args import Global
import utils

# Libraries
import cv2
import imageio
from PIL import Image

# Standard
from pathlib import Path
import random

def get_frames(num_frames):
	frames = []
	ext = utils.get_extension(Global.input)

	if ext == ".jpg" or ext == ".png":
		for x in range(0, num_frames):
			frame = cv2.imread(str(Global.input))
			frames.append(frame)
	else:
		cap = cv2.VideoCapture(str(Global.input))
		total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		current = 0

		# Sometimes it fails to read the frames so it needs more tries
		for x in range(0, num_frames * 25):
			if Global.order == "normal":
				index = current
			elif Global.order == "random":
				index = random.choice(range(total_frames))

			cap.set(cv2.CAP_PROP_POS_FRAMES, index)
			ret, frame = cap.read()

			if ret:
				frames.append(frame)

			if len(frames) == num_frames:
				break

			current += 1

			if current >= total_frames:
				current = 0

		cap.release()

	return frames

def add_text(frame, text, lineheight):
	if not text:
		return frame, 0

	height, width, _ = frame.shape

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

	if Global.bgcolor:
		if Global.no_baseline:
			bline = 0
		else:
			bline = baseline

		padding = Global.padding
		rect_x = text_x - padding
		rect_y = text_y - text_height - padding
		rect_width = padding + text_width + padding
		rect_height = padding + text_height + bline + padding
		rect_1 = (rect_x, rect_y)
		rect_2 = (rect_x + rect_width, rect_y + rect_height)
		rcopy = cv2.rectangle(frame.copy(), rect_1, rect_2, Global.bgcolor, -1)
		cv2.addWeighted(frame, 1 - Global.opacity, rcopy, Global.opacity, 0, frame)

	cv2.putText(frame, text, text_position, font, Global.fontsize, Global.fontcolor, Global.boldness, cv2.LINE_AA)
	return frame, text_height

def word_frames(frames):
	if len(Global.words) == 0:
		return frames

	worded = []

	for i, frame in enumerate(frames):
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
		ratio = frame.shape[1] / frame.shape[0]
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
		frames[0].save(output, save_all=True, append_images=frames[1:], duration=Global.delay, loop=loop, optimize=True)
	elif fmt == "mp4":
		imageio.mimsave(output, frames, fps=Global.fps, quality=Global.quality)

	print(f"\nSaved as: {output}\n")

def check_frames():
	num = len(Global.words)
	Global.frames = num if num > 0 else Global.frames

def fix_frames(frames):
	new_frames = []

	for frame in frames:
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(rgb_frame)
		new_frames.append(pil_image)

	return new_frames