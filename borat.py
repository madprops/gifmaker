import cv2
import imageio
import numpy as np
import os
import random
import string

VIDEO = "video.webm"
FRAMES = 3
DELAY = 180
RIGHT = 45
BOTTOM = 100

def get_frames():
	cap = cv2.VideoCapture(VIDEO)
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	words = get_random_words(FRAMES)
	frames_done = []

	# Sometimes it fails to read the frames so it needs more tries
	for x in range(0, FRAMES * 100):
		index = random.choice(range(total_frames))
		cap.set(cv2.CAP_PROP_POS_FRAMES, index)
		ret, frame = cap.read()

		if ret:
			frames_done.append(add_text(frame, words[len(frames_done)]))

		if len(frames_done) == FRAMES:
			break

	cap.release()

	if len(frames_done) > 0:
		create_gif(frames_done)

def add_text(frame, text):
	height, width, _ = frame.shape
	font = cv2.FONT_HERSHEY_SIMPLEX
	scale = 3
	thickness = 3
	text_size = cv2.getTextSize(text, font, scale, thickness)[0]
	text_position = (width - text_size[0] - RIGHT, height - BOTTOM)
	cv2.putText(frame, text, text_position, font, scale, (255, 255, 255), thickness, cv2.LINE_AA)
	return frame

def get_random_words(num_words):
	dict_words = "/usr/share/dict/words"

	with open(dict_words, "r") as file:
		words = file.read().splitlines()
		return random.sample(words, num_words)

def create_gif(frames):
	fname = random_string()
	output = f"output/{fname}.gif"
	duration = len(frames) * DELAY
	os.makedirs("output", exist_ok=True)
	imageio.mimsave(output, frames, duration=duration, loop=0)

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

if __name__ == "__main__":
	get_frames()