# Modules
from configuration import config
import words
import media


def main() -> None:
    # Fill some paths based on root path
    config.fill_paths(__file__)

    # Check the provided arguments
    config.parse_args()

    if not config.remake:
        # Replace [empty]
        words.replace_empty()

        # Replace [random] and [number]
        words.replace_random()

        # Replace [date]
        words.replace_date()

        # Replace [repeat]
        words.replace_repeat()

        # Replace [count]
        words.replace_count()

    # Extract the required frames from the file
    frames = media.get_frames()

    if config.remake:
        # Only resize the frames
        frames = media.resize_frames(frames)
    else:
        # Apply filters to all the frames
        frames = media.apply_filters(frames)

        # Add the words to the frames
        frames = media.word_frames(frames)

        # Resize the frames based on width
        frames = media.resize_frames(frames)

    # Render and save the output
    output = media.render(frames)
    print(output)


if __name__ == "__main__":
    main()
