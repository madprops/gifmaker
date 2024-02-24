# Modules
from configuration import config
import words
import media
import utils

# Standard
import time

# Performance
last_time: float = 0

def check_time(section: str) -> None:
    if not config.verbose:
        return

    global last_time
    now = time.time()
    diff = round(now - last_time, 3)
    utils.msg(f"{section}: {diff} seconds")
    last_time = now

def main() -> None:
    global last_time
    start_time = time.time()
    last_time = start_time

    # Fill some paths based on root path
    config.fill_paths(__file__)

    # Check the provided arguments
    config.parse_args()
    check_time("Parse Args")

    if not config.remake:
        # Replace [empty]
        words.replace_empty()
        check_time("Replace Empty")

        # Replace [random] and [number]
        words.replace_random()
        check_time("Replace Random")

        # Replace [date]
        words.replace_date()
        check_time("Replace Date")

        # Replace [repeat]
        words.replace_repeat()
        check_time("Replace Repeat")

        # Replace [count]
        words.replace_count()
        check_time("Replace Count")

    # Extract the required frames from the file
    frames = media.get_frames()
    check_time("Get Frames")

    if config.remake:
        # Only resize the frames
        frames = media.resize_frames(frames)
        check_time("Resize Frames")
    else:
        # Apply filters to all the frames
        frames = media.apply_filters(frames)
        check_time("Apply Filters")

        # Add the words to the frames
        frames = media.word_frames(frames)
        check_time("Word Frames")

        # Resize the frames based on width
        frames = media.resize_frames(frames)
        check_time("Resize Frames")

    # Render and save the output
    output = media.render(frames)
    check_time("Render")

    # End stats
    if config.verbose:
        total = round(time.time() - start_time, 3)
        utils.msg(f"\nFrames: {len(frames)}")
        utils.msg(f"Total: {total} seconds\n")

    # Print the output path as the response
    print(output)


if __name__ == "__main__":
    main()
