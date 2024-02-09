# Modules
import utils

# Libraries
import cv2
import imageio

# Standard
import random
import argparse
from pathlib import Path

# Frames per second to use
FPS = 2.2

# Number of frames to use if no words are provided
FRAMES = 3

# The size of the text
SIZE = 3

# The thickness of the text
THICK = 3

# The padding from the left
LEFT = None

# The padding from the top
TOP = None

# The width to resize the frames
WIDTH = None

# The directory where this file resides
HERE = Path(__file__).parent

# Default path to the video file
VIDEO = Path(HERE, "video.webm")

# Default words to use
WORDS = []

# The separator to use when splitting word lines
SEP = ";"

def get_frames(num_frames):
	cap = cv2.VideoCapture(str(VIDEO))
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
	text_size = cv2.getTextSize(text, font, SIZE, THICK)[0]

	if LEFT is not None:
		text_x = LEFT
	else:
		text_x = (width - text_size[0]) // 2

	if TOP is not None:
		text_y = text_size[1] + TOP
	else:
		text_y = (height + text_size[1]) // 2

	text_position = (text_x, text_y)
	cv2.putText(frame, text, text_position, font, SIZE, (255, 255, 255), THICK, cv2.LINE_AA)
	return frame

def word_frames(frames):
	worded = []

	for i, frame in enumerate(frames):
		worded.append(add_text(frame, WORDS[i]))

	return worded

def resize_frames(frames):
	if WIDTH is None:
		return frames

	new_frames = []

	for frame in frames:
		ratio = frame.shape[1] / frame.shape[0]
		height = int(WIDTH / ratio)
		new_frames.append(cv2.resize(frame, (WIDTH, height)))

	return new_frames

def create_gif(frames):
	rand = utils.random_string()
	file_name = f"{rand}.gif"
	output_dir = Path(HERE, "output")
	output_dir.mkdir(parents=False, exist_ok=True)
	output = Path(output_dir, file_name)
	imageio.mimsave(output, frames, fps=FPS, loop=0)

def check_args():
	global VIDEO
	global FRAMES
	global WORDS
	global FPS
	global SIZE
	global THICK
	global LEFT
	global TOP
	global WIDTH

	parser = argparse.ArgumentParser(description="Borat the Gif Maker")

	parser.add_argument("--video", type=str, help="Path to the video file")
	parser.add_argument("--words", type=str, help=f"Words to use. Use [random] to use a random word. Separate lines with {SEP}")
	parser.add_argument("--fps", type=float, help="FPS to use")
	parser.add_argument("--left", type=int, help="Right padding")
	parser.add_argument("--top", type=int, help="Bottom padding")
	parser.add_argument("--width", type=int, help="Width to resize the frames")
	parser.add_argument("--size", type=float, help="Text size")
	parser.add_argument("--thick", type=int, help="Text thickness")
	parser.add_argument("--frames", type=int, help="Number of frames to use if no words are provided")

	args = parser.parse_args()

	if args.video is not None:
		VIDEO = Path(args.video)

	if args.words is not None:
		WORDS = [word.strip() for word in args.words.split(SEP)]
		FRAMES = len(WORDS)
	elif args.frames is not None:
		FRAMES = args.frames

	if args.fps is not None:
		FPS = args.fps

	if args.size is not None:
		SIZE = args.size

	if args.thick is not None:
		THICK = args.thick

	if args.left is not None:
		LEFT = args.left

	if args.top is not None:
		TOP = args.top

	if args.width is not None:
		WIDTH = args.width

def check_random():
	if len(WORDS) == 0:
		return

	rs_lower = "[random]"
	rs_upper = "[RANDOM]"
	rs_title = "[Random]"

	num_random = 0

	for rs in [rs_lower, rs_upper, rs_title]:
		num_random += sum(w.count(rs) for w in WORDS)

	if num_random == 0:
		return

	randwords = utils.random_words(num_random)

	def get_rand():
		return randwords.pop(0)

	for i, line in enumerate(WORDS):
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

		WORDS[i] = " ".join(new_words)

def main():
	check_args()
	check_random()

	frames = get_frames(FRAMES)

	if len(frames) == 0:
		return

	if len(WORDS) > 0:
		frames = word_frames(frames)

	frames = resize_frames(frames)
	create_gif(frames)

if __name__ == "__main__":
	main()