# Modules
from args import Global
import args
import words
import media

def main():
	args.fill_paths(__file__)

	args.parse_args()
	words.check_random()
	words.check_repeat()
	media.check_frames()

	frames = media.get_frames(Global.frames)
	frames = media.word_frames(frames)
	frames = media.resize_frames(frames)

	media.render(frames)

if __name__ == "__main__":
	main()