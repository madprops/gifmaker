# Modules
from config import Global
import config
import args
import words
import media

def main():
	config.fill_paths(__file__)
	args.check()

	if not Global.input.exists():
		return

	words.check_random()
	words.check_repeat()

	frames = media.get_frames(Global.frames)

	if len(frames) == 0:
		return

	if len(Global.words) > 0:
		frames = media.word_frames(frames)

	frames = media.resize_frames(frames)
	media.render(frames)

if __name__ == "__main__":
	main()