# Modules
from configuration import config
import words
import media

# Libraries
import random
from pathlib import Path

def main() -> None:
	# Fill some paths based on root path
	config.fill_paths(Path(__file__))

	# Check the provided arguments
	config.parse_args()

	# Replace [empty] with empty lines
	words.check_empty()

	# Replace [random] with random words
	words.check_random()

	# Replace [repeat] with repeated lines
	words.check_repeat()

	# Check how many frames to extract
	media.count_frames()

	# Pick one input path randomly
	path = random.choice(config.input)

	# Extract the required frames from the file
	frames = media.get_frames(path)

	if config.remake:
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
	output = media.render(frames)
	print(output)

if __name__ == "__main__":
	main()