# Standard
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
	here = None

	# Default path to the video file
	video = None

	# The output directory
	outdir = None

	# Default words to use
	words = []

	# The separator to use when splitting word lines
	sep = ";"

	# The list of nouns to use
	nouns = []

def fill_paths(here):
	Global.here = here
	Global.video = Path(here, "media", "video.webm")
	Global.outdir = Path(here, "output")