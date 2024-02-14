# Modules
from args import Global
import args
import words
import media

# Libraries
import random

def main():
	args.fill_paths(__file__)
	args.parse_args()
	words.check_random()
	words.check_repeat()

	# Pick one input path randomly
	path = random.choice(Global.input)

	# Extract the required frames from the file
	frames = media.get_frames(path)

	if Global.resize:
		# Only resize the frames
		frames = media.resize_frames(frames)
	else:
		# Do all the operations
		frames = media.apply_filters(frames)
		frames = media.word_frames(frames)
		frames = media.resize_frames(frames)

	media.render(frames)

if __name__ == "__main__":
	main()