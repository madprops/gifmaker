# Modules
from configuration import config
import words
import media
import utils

# Standard
import time

# Performance
last_time = 0.0


def get_time() -> float:
    return time.time()


def show_seconds(name: str, start: float, end: float) -> None:
    num = round(start - end, 3)
    label = utils.colortext("blue", name)
    utils.msg(f"{label}: {num} seconds")


def check_time(name: str) -> None:
    if not config.verbose:
        return

    global last_time
    now = get_time()
    show_seconds(name, now, last_time)
    last_time = now


def main() -> None:
    global last_time

    start_time = get_time()
    last_time = start_time

    # Fill some paths based on root path
    config.fill_paths(__file__)

    # Check the provided arguments
    config.parse_args()
    check_time("Parse Args")

    # Process words
    words.process_words()
    check_time("Process Words")

    # Extract the required frames from the file
    frames = media.get_frames()
    check_time("Get Frames")

    if not frames:
        utils.msg("No frames")
        return

    if config.remake:
        # Only resize the frames
        frames = media.resize_frames(frames)
        check_time("Resize Frames")
    else:
        # Apply filters to all the frames
        frames = media.apply_filters(frames)
        check_time("Apply Filters")

        # Deep Fry frames if enabled
        frames = media.deep_fry(frames)
        check_time("Deep Fry")

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
        utils.msg("")
        label = utils.colortext("blue", "Frames")
        utils.msg(f"{label}: {len(frames)}")
        show_seconds("Total", get_time(), start_time)
        utils.msg("")

    # Print the output path as the response
    print(output)


if __name__ == "__main__":
    main()
