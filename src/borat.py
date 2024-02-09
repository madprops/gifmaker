# Modules
from config import Global
import config
import utils
import args

# Libraries
import cv2
import imageio

# Standard
import random
from pathlib import Path

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

def add_text(frame, text):
	if not text.split():
		return frame

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

	text_size = cv2.getTextSize(text, font, Global.fontsize, Global.boldness)[0]

	if Global.left is not None:
		text_x = Global.left
	elif Global.right is not None:
		text_x = width - text_size[0] - Global.right
	else:
		text_x = (width - text_size[0]) // 2

	if Global.top is not None:
		text_y = text_size[1] + Global.top
	elif Global.bottom is not None:
		text_y = height - (text_size[1] // 2)
	else:
		text_y = (height + text_size[1]) // 2

	text_position = (text_x, text_y)
	cv2.putText(frame, text, text_position, font, Global.fontsize, (255, 255, 255), Global.boldness, cv2.LINE_AA)
	return frame

def word_frames(frames):
	worded = []

	for i, frame in enumerate(frames):
		worded.append(add_text(frame, Global.words[i]))

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

	if ext:
		try:
			Global.output.parent.mkdir(parents=False, exist_ok=True)
		except:
			return

		output = Global.output
	else:
		try:
			Global.output.mkdir(parents=False, exist_ok=True)
		except:
			return

		rand = utils.random_string()
		file_name = f"{rand}.{Global.format}"
		output = Path(Global.output, file_name)

	fmt = ext if ext else Global.format

	if fmt == "gif":
		imageio.mimsave(output, frames, fps=Global.fps, loop=0)
	elif fmt == "mp4":
		imageio.mimsave(output, frames, fps=Global.fps)

	print(f"\nSaved as: {output}\n")

def check_random():
	if len(Global.words) == 0:
		return

	rs_lower = "[random]"
	rs_upper = "[RANDOM]"
	rs_title = "[Random]"

	num_random = 0

	for rs in [rs_lower, rs_upper, rs_title]:
		num_random += sum(w.count(rs) for w in Global.words)

	if num_random == 0:
		return

	for i, line in enumerate(Global.words):
		new_words = []

		for word in line.split():
			new_word = word

			if word == rs_lower:
				new_word = utils.random_word().lower()
			elif word == rs_upper:
				new_word = utils.random_word().upper()
			elif word == rs_title:
				new_word = utils.random_word().title()

			new_words.append(new_word)

		Global.words[i] = " ".join(new_words)

def main():
	config.fill_paths(Path(__file__).parent)

	args.check()

	if not Global.input.exists():
		return

	check_random()

	frames = get_frames(Global.frames)

	if len(frames) == 0:
		return

	if len(Global.words) > 0:
		frames = word_frames(frames)

	frames = resize_frames(frames)
	render(frames)

if __name__ == "__main__":
	main()