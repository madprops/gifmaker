# Modules
from config import Global
import config
import args
import words
import media

def main():
	config.fill_paths(__file__)
	args.check()

	words.check_random()
	words.check_repeat()
	media.check_frames()

	frames = media.get_frames(Global.frames)
	frames = media.word_frames(frames)
	frames = media.resize_frames(frames)

	media.render(frames)

if __name__ == "__main__":
	main()