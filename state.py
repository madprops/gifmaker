from pathlib import Path
from dataclasses import dataclass

@dataclass
class Global:
	# Frames per second to use
	fps = 2.2

	# Number of frames to use if no words are provided
	frames = 3

	# The size of the text
	size = 3

	# The thickness of the text
	thick = 3

	# The padding from the left
	left = None

	# The padding from the top
	top = None

	# The width to resize the frames
	width = None

	# The directory where this file resides
	here = Path(__file__).parent

	# Default path to the video file
	video = Path(here, "video.webm")

	# Default words to use
	words = []

	# The separator to use when splitting word lines
	sep = ";"

	# The list of nouns to use
	nouns = []