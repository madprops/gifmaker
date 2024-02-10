# Modules
from config import Global
import utils

# Standard
import argparse
from pathlib import Path

def check():
	p = argparse.ArgumentParser(description="Borat the Gif Maker")

	p.add_argument("--input", "-i", type=str, help="Path to the a video or image file")
	p.add_argument("--words", type=str, help=f"Lines of words to use on the frames")
	p.add_argument("--fps", type=float, help="FPS to use")
	p.add_argument("--left", type=int, help="Left padding")
	p.add_argument("--right", type=int, help="Right padding")
	p.add_argument("--top", type=int, help="Top padding")
	p.add_argument("--bottom", type=int, help="Bottom padding")
	p.add_argument("--width", type=int, help="Width to resize the frames")
	p.add_argument("--fontsize", type=float, help="Text size")
	p.add_argument("--boldness", type=int, help="Text thickness")
	p.add_argument("--frames", type=int, help="Number of frames to use if no words are provided")
	p.add_argument("--output", "-o", type=str, help="Output directory to save the file")
	p.add_argument("--format", type=str, choices=["gif", "mp4"], help="The format of the output file")
	p.add_argument("--separator", type=str, help="Character to use as the separator")
	p.add_argument("--order", type=str, choices=["random", "normal"], help="The order to use when extracting the frames")
	p.add_argument("--font", type=str, choices=["simple", "complex", "plain", "duplex", "triplex"], help="The font to use for the text")

	args = p.parse_args()

	def proc(attr, value):
		if value is not None:
			setattr(Global, attr, value)

	proc(Global.separator, args.separator)

	if args.words is not None:
		Global.words = [word.strip() for word in args.words.split(Global.separator)]
		Global.frames = len(Global.words)
	elif args.frames is not None:
		Global.frames = args.frames

	proc("fps", args.fps)
	proc("fontsize", args.fontsize)
	proc("boldness", args.boldness)
	proc("left", args.left)
	proc("right", args.right)
	proc("top", args.top)
	proc("bottom", args.bottom)
	proc("width", args.width)
	proc("format", args.format)
	proc("order", args.order)
	proc("font", args.font)

	if args.input is not None:
		Global.input = utils.resolve_path(args.input)

	if args.output is not None:
		Global.output = utils.resolve_path(args.output)