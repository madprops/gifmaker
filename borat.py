import sys
import cv2
import imageio
import os
import random
import string

VIDEO = "video.webm"
DELAY = 500
RIGHT = 45
BOTTOM = 100
WORDS = []
RAND_WORDS = 3
SCALE = 3
THICK = 3

def get_frames(num_frames):
	cap = cv2.VideoCapture(VIDEO)
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
	height, width, _ = frame.shape
	font = cv2.FONT_HERSHEY_SIMPLEX
	text_size = cv2.getTextSize(text, font, SCALE, THICK)[0]
	text_position = (width - text_size[0] - RIGHT, height - BOTTOM)
	cv2.putText(frame, text, text_position, font, SCALE, (255, 255, 255), THICK, cv2.LINE_AA)
	return frame

def get_random_words(num_words):
	dict_words = "/usr/share/dict/words"

	with open(dict_words, "r") as file:
		words = file.read().splitlines()
		return random.sample(words, num_words)

def create_gif(frames):
	fname = random_string()
	output = f"output/{fname}.gif"
	os.makedirs("output", exist_ok=True)
	imageio.mimsave(output, frames, duration=DELAY, loop=0)

def random_string():
	vowels = "aeiou"
	consonants = "".join(set(string.ascii_lowercase) - set(vowels))

	return (
		random.choice(consonants) +
		random.choice(vowels) +
		random.choice(consonants) +
		random.choice(vowels) +
		random.choice(consonants) +
		random.choice(vowels)
	)

def word_frames(frames):
	worded = []

	for i, frame in enumerate(frames):
		worded.append(add_text(frame, WORDS[i]))

	return worded

def is_number(s):
	try:
		return int(s)
	except:
		return 0

def check_args():
	global WORDS
	global RAND_WORDS

	if len(sys.argv) > 1:
		arg = sys.argv[1]
		num = is_number(arg)

		if num > 0:
			RAND_WORDS = num
		else:
			wordstr = arg.split()
			WORDS = [word for word in wordstr if word]

	if len(WORDS) == 0:
		WORDS = get_random_words(RAND_WORDS)

def main():
	check_args()
	frames = get_frames(len(WORDS))

	if len(frames) == 0:
		return

	worded = word_frames(frames)
	create_gif(worded)

if __name__ == "__main__":
	main()