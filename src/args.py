# Modules
from config import Global
import utils

# Standard
import argparse
from pathlib import Path

def check():
	parser = argparse.ArgumentParser(description="Borat the Gif Maker")

	parser.add_argument("--input", "-i", type=str, help="Path to the a video or image file")
	parser.add_argument("--words", type=str, help=f"Lines of words to use on the frames")
	parser.add_argument("--fps", type=float, help="FPS to use")
	parser.add_argument("--left", type=int, help="Left padding")
	parser.add_argument("--right", type=int, help="Right padding")
	parser.add_argument("--top", type=int, help="Top padding")
	parser.add_argument("--bottom", type=int, help="Bottom padding")
	parser.add_argument("--width", type=int, help="Width to resize the frames")
	parser.add_argument("--fontsize", type=float, help="Text size")
	parser.add_argument("--boldness", type=int, help="Text thickness")
	parser.add_argument("--frames", type=int, help="Number of frames to use if no words are provided")
	parser.add_argument("--output", "-o", type=str, help="Output directory to save the file")
	parser.add_argument("--ext", type=str, help="The format of the output file. Either gif or mp4")
	parser.add_argument("--separator", type=str, help="Character to use as the separator")
	parser.add_argument("--order", type=str, help="The order to use when extracting the frames. Either random or normal")
	parser.add_argument("--font", type=str, help="The font to use for the text. Either simple, complex, plain, duplex, or triplex")

	args = parser.parse_args()

	if args.input is not None:
		Global.input = utils.resolve_path(args.input)

	if args.separator is not None:
		Global.separator = args.separator

	if args.words is not None:
		Global.words = [word.strip() for word in args.words.split(Global.separator)]
		Global.frames = len(Global.words)
	elif args.frames is not None:
		Global.frames = args.frames

	if args.fps is not None:
		Global.fps = args.fps

	if args.fontsize is not None:
		Global.fontsize = args.fontsize

	if args.boldness is not None:
		Global.boldness = args.boldness

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

	if args.output is not None:
		Global.output = utils.resolve_path(args.output)

	if args.ext is not None:
		Global.ext = args.ext

	if args.order is not None:
		Global.order = args.order

	if args.font is not None:
		Global.font = args.font