<img src="media/borat.jpg" width="380">

This is a python program to produce gif images (or videos).

It extracts random (or sequential) frames from a video (or image).

It (optionally) places words somewhere on each frame.

Then joins all frames into an animated gif (or mp4).

---

## Why?

It might be useful in the realm of human verification.

And memes.

---

## Index
1. [Installation](#installation)
1. [Usage](#usage)
1. [Arguments](#arguments)

---

<img src="media/installation.gif">

---

## Installation <a name="installation"></a>

Clone this repo, and get inside the directory:

```
git clone --depth=1 https://github.com/madprops/borat

cd borat
```

Then create the virtual env:

```
python -m venv venv
```

Then install the dependencies:

```
venv/bin/pip install -r requirements.txt
```

Or simply run `install.sh` to create the virtual env and install the dependencies.

There's a `test.sh` file that runs borat with some pre-defined flags to test if things are working properly.

---

<img src="media/usage.gif">

---

## Usage <a name="usage"></a>

Run `src/borat.py` using the python in the virtual env:

```
venv/bin/python src/borat.py
```

You can provide a video or image path using the `--input` flag:

```
venv/bin/python src/borat.py --input="/path/to/video.webm"
venv/bin/python src/borat.py --input="/path/to/image.png"
```

`webm`, `mp4`, `gif`, `jpg`, and `png` should work, and maybe other formats.

You can pass it a string of lines to use on each frame.

They are separated by `;` (semicolons).

```
venv/bin/python src/borat.py --words="Hello Brother ; Construct Additional Pylons"
```

It will make 2 frames, one per line.

If you want to use words and have some frames without them simply use more `;`.

---

You can use random words with `[random]`:

```
venv/bin/python src/borat.py --words="I Like [random] and [random]"
```

It will pick random words from a list of english words.

There are 3 kinds of random formats: `[random]`, `[RANDOM]`, and `[Random]`.

The replaced word will use the case of those.

For example `[RANDOM]` might be `PLANET`.

---

If you want to repeat the text in the next frame use `[again]` in a line.

For example `--words="Buy Buttcoin ; [again] ;;"`

It will use that text on the first two frames and then show 2 empty frames.

---

You can run `borat.py` from anywhere in your system using its virtual env.

Relative paths should work fine.

---

Here's a fuller example:

```
venv/bin/python src/borat.py --input="/videos/stuff.webm" --fontsize=3.3 --fps=1.5 --width=600 --words="I want to eat ;; [Random] ; [again] ;" --format=mp4 --output="stuff/videos"
```

---

<img src="media/arguments.gif">

---

## Arguments <a name="arguments"></a>

You can use flag arguments like: `--fps=2.4 --width=500 --order=normal`

These modify how the file is going to be generated.

---

> input = Type: str | Default: The included example video

Which video or image to use as the source of the frames.

`webm`, `mp4`, `gif`, and even `jpg` or `png` should work.

For example: `stuff/cow.mp4`

`-i` is a shorter alias for this.

---

> output = Type: str | Default: The borat/output directory

In which directoy to save the generated file.

For example: `stuff/videos`

It will use a random file name.

Using `gif` or `mp4` depending on the `format` argument.

Or you can enter the path plus the file name.

For example: `stuff/videos/cat.gif`

The format is deduced by the extension (gif or mp4).

`-o` is a shorter alias for this.

---

> words = Type: str | Default: No words

The words string to use.

Lines are separated by `;`.

Special words include `[random]` and `[again]`.

As described in [Usage](#usage).

---

> fps = Type: float | Default: 2.0

(Frames Per Second) modifies the speed between frame change (ms).

A bigger `fps` = A faster gif.

---

> frames = Type: int | Default: 3

The amount of frames to use if `--words` is not used.

---

> left = Type: int | Default: None

Padding from the left edge to position the text.

---

> right = Type: int | Default: None

Padding from the right edge to position the text.

---

> top = Type: int | Default: None

Padding from the top edge to position the text.

---

> bottom = Type: int | Default: None

Padding from the bottom edge to position the text.

---

You only need to set `left` or `right`, not both.

You only need to set `top` or `bottom`, not both.

If those are not set then the text is placed at the center.

---

> width = Type: int | Default: None

Fixed width to every frame. Height is always automatic.

---

> format = Type: str | Default: "gif"

The format of the output file. Either `gif` or `mp4`.

This is only used when the output is not a direct file path.

For instance if the output ends with `cat.gif` it will use `gif`.

If the output is a directory it will use a random name with the appropiate format.

---

> separator = Type: str | Default: ";"

Which character to consider as the separator in `words`.

---

> order = Type: str | Default: "random"

The order used to extract the frames.

Either `random` or `normal`.

`random` picks frames randomly.

`normal` picks frames in order starting from the first one.

`normal` loops back to the first frame if needed.

---

> font = Type: str | Default "simple"

The font to use for the text.

Either `simple`, `complex`, `plain`, `duplex`, or `triplex`.

---

> fontsize = Type: float | Default: 3.0

The size of the text.

---

> fontcolor = Type: str | Default: "255,255,255"

The color of the text.

3 numbers from `0` to `255`, separated by commas.

`0,0,0` would be black, for instance.

---

> boldness = Type: int | Default: 3

The thickness of the text.

---

<img src="media/borat.gif" width="600">

---

Borat Sagdiyev, born on May 27, 1972, is a cultural figure known for his distinctive style and comedic persona. Originating from the village of Kuzcek in Kazakhstan, Borat gained prominence as a journalist and television personality. His early life was marked by a fascination with performance arts and humor, and he showcased his talents at local events, earning the admiration of his community.

Borat pursued higher education in journalism at Kazakh State University, reflecting his curiosity about the world beyond his homeland. His professional journey led him to become a television reporter for Kazakh Television, where he contributed to the state-run network. Over time, he gained recognition and was selected by the government to represent Kazakhstan in various international events, showcasing the nation's culture and traditions.

Borat's unconventional approach and distinctive sense of humor made him a memorable character, both locally and internationally. His interactions with people from different cultures, documented in a unique documentary-style film, provided a humorous and, at times, controversial perspective on cultural differences and stereotypes.

Beyond his on-screen exploits, Borat became a cultural icon, sparking discussions about the boundaries of satire and the impact of media on public perception. His legacy endures as a testament to the power of comedy to navigate complex social issues and challenge preconceived notions.