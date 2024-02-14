# Modules
from args import Global
import args
import words
import media

# Libraries
import random

def main():
	# Fill some paths based on root path
	args.fill_paths(__file__)

	# Check the provided arguments
	args.parse_args()

	# Replace [random] with random words
	words.check_random()

	# Replace [repeat] with repeated lines
	words.check_repeat()

	# Check how many frames to extract
	media.count_frames()

	# Pick one input path randomly
	path = random.choice(Global.input)

	# Extract the required frames from the file
	frames = media.get_frames(path)

	if Global.resize:
		# Only resize the frames
		frames = media.resize_frames(frames)
	else:
		# Apply filters to all the frames
		frames = media.apply_filters(frames)

		# Add the words to the frames
		frames = media.word_frames(frames)

		# Resize the frames based on width
		frames = media.resize_frames(frames)

	# Render and save the output
	media.render(frames)

if __name__ == "__main__":
	main()