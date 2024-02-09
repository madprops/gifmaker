# Modules
from state import Global
import utils

# Libraries
import cv2
import imageio

# Standard
import random
import argparse
from pathlib import Path

def get_frames(num_frames):
	cap = cv2.VideoCapture(str(Global.video))
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frames = []

	# Sometimes it fails to read the frames so it needs more tries
	for x in range(0, num_frames * 25):
		index = random.choice(range(total_frames))
		cap.set(cv2.CAP_PROP_POS_FRAMES, index)
		ret, frame = cap.read()

		if ret:
			frames.append(frame)

		if len(frames) == num_frames:
			break

	cap.release()
	return frames

def add_text(frame, text):
	if not text.split():
		return frame

	height, width, _ = frame.shape
	font = cv2.FONT_HERSHEY_SIMPLEX
	text_size = cv2.getTextSize(text, font, Global.size, Global.thick)[0]

	if Global.left is not None:
		text_x = Global.left
	else:
		text_x = (width - text_size[0]) // 2

	if Global.top is not None:
		text_y = text_size[1] + Global.top
	else:
		text_y = (height + text_size[1]) // 2

	text_position = (text_x, text_y)
	cv2.putText(frame, text, text_position, font, Global.size, (255, 255, 255), Global.thick, cv2.LINE_AA)
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

def create_gif(frames):
	rand = utils.random_string()
	file_name = f"{rand}.gif"
	output_dir = Path(Global.here, "output")
	output_dir.mkdir(parents=False, exist_ok=True)
	output = Path(output_dir, file_name)
	imageio.mimsave(output, frames, fps=Global.fps, loop=0)

def check_args():
	parser = argparse.ArgumentParser(description="Borat the Gif Maker")

	parser.add_argument("--video", type=str, help="Path to the video file")
	parser.add_argument("--words", type=str, help=f"Words to use. Use [random] to use a random word. Separate lines with {Global.sep}")
	parser.add_argument("--fps", type=float, help="FPS to use")
	parser.add_argument("--left", type=int, help="Right padding")
	parser.add_argument("--top", type=int, help="Bottom padding")
	parser.add_argument("--width", type=int, help="Width to resize the frames")
	parser.add_argument("--size", type=float, help="Text size")
	parser.add_argument("--thick", type=int, help="Text thickness")
	parser.add_argument("--frames", type=int, help="Number of frames to use if no words are provided")

	args = parser.parse_args()

	if args.video is not None:
		Global.video = Path(args.video)

	if args.words is not None:
		Global.words = [word.strip() for word in args.words.split(Global.sep)]
		Global.frames = len(Global.words)
	elif args.frames is not None:
		Global.frames = args.frames

	if args.fps is not None:
		Global.fps = args.fps

	if args.size is not None:
		Global.size = args.size

	if args.thick is not None:
		Global.thick = args.thick

	if args.left is not None:
		Global.left = args.left

	if args.top is not None:
		Global.top = args.top

	if args.width is not None:
		Global.width = args.width

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

	randwords = utils.random_words(num_random)

	def get_rand():
		return randwords.pop(0)

	for i, line in enumerate(Global.words):
		new_words = []

		for word in line.split():
			new_word = word

			if word == rs_lower:
				new_word = get_rand().lower()
			elif word == rs_upper:
				new_word = get_rand().upper()
			elif word == rs_title:
				new_word = get_rand().title()

			new_words.append(new_word)

		Global.words[i] = " ".join(new_words)

def main():
	check_args()
	check_random()

	frames = get_frames(Global.frames)

	if len(frames) == 0:
		return

	if len(Global.words) > 0:
		frames = word_frames(frames)

	frames = resize_frames(frames)
	create_gif(frames)

if __name__ == "__main__":
	main()