# Modules
from state import Global

# Standard
import argparse
from pathlib import Path

def check():
	parser = argparse.ArgumentParser(description="Borat the Gif Maker")

	parser.add_argument("--input", type=str, help="Path to the a video or image file")
	parser.add_argument("--words", type=str, help=f"Words to use. Use [random] to use a random word. Separate lines with {Global.separator}")
	parser.add_argument("--fps", type=float, help="FPS to use")
	parser.add_argument("--left", type=int, help="Left padding")
	parser.add_argument("--right", type=int, help="Right padding")
	parser.add_argument("--top", type=int, help="Top padding")
	parser.add_argument("--bottom", type=int, help="Bottom padding")
	parser.add_argument("--width", type=int, help="Width to resize the frames")
	parser.add_argument("--size", type=float, help="Text size")
	parser.add_argument("--thick", type=int, help="Text thickness")
	parser.add_argument("--frames", type=int, help="Number of frames to use if no words are provided")
	parser.add_argument("--outdir", type=str, help="Output directory to save the gif")
	parser.add_argument("--ext", type=str, help="The format of the output file. Either gif or mp4")

	args = parser.parse_args()

	if args.input is not None:
		Global.input = Path(args.input)

	if args.words is not None:
		Global.words = [word.strip() for word in args.words.split(Global.separator)]
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

	if args.right is not None:
		Global.right = args.right

	if args.top is not None:
		Global.top = args.top

	if args.bottom is not None:
		Global.bottom = args.bottom

	if args.width is not None:
		Global.width = args.width

	if args.outdir is not None:
		Global.outdir = Path(args.outdir)

	if args.ext is not None:
		Global.ext = args.ext