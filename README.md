<img src="media/borat.jpg" width="350">

This is a python program to produce gif images (or videos).

It extracts random (or sequential) frames from a video (or image).

It (optionally) places words somewhere on each frame.

Then joins all frames into an animated gif (or mp4).

## Why?

It might be useful in the realm of human verification.

And memes.

## Index
1. [Installation](#installation)
1. [Usage](#usage)
1. [Arguments](#arguments)

---

<img src="media/installation.gif">

---

## Installation <a name="installation"></a>

Clone this repo, and get inside the dir.

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
venv/bin/python src/borat.py --input="/path/to/image.png
```

`webm`, `mp4`, and `gif` should work, and maybe other formats.

You can pass it a string of lines to use on each frame.

They are separated by ";" (semicolons).

```
venv/bin/python src/borat.py --words="Hello Brother; Construct Additional Pylons"
```

It will make 2 frames, one per line.

If you want to make a gif with 5 random frames and an FPS of 3:

```
venv/bin/python src/borat.py --frames=5 --fps=3
```

You can use random words with `[random]`:

```
venv/bin/python src/borat.py --words="I Like [random] and [random]"
```

It will pick random words from a list of english words.

There are 3 kinds of random formats: `[random]`, `[RANDOM]`, and `[Random]`.

The replaced word will use the casing of those.

For example `[RANDOM]` might be `PLANET`.

If you want to use words and have some frames without them simply use more `;`.

Here's a fuller example:

```
venv/bin/python src/borat.py --input="/videos/stuff.webm" --fontsize=3 --fps=1.5 --width=600 --words="; I want to eat;; [Random] --format="mp4"
```

You can run `borat.py` from anywhere in your system using its virtual env. Relative paths should work fine.

---

<img src="media/arguments.gif">

---

## Arguments <a name="arguments"></a>

You can use flag arguments like: `--fps=3 --top=0 --width=500`

These modify how the gif image is going to be generated.

---

> fps = Type: Float | Default: 2.0

(Frames Per Second) modifies the speed between frame change (ms).

A bigger `fps` = A faster gif.

---

> frames = Type: Int | Default: 3

The amount of frames to use if `--words` is not used.

---

> left = Type: Int | Default: None

Padding from the left edge to position the text.

---

> right = Type: Int | Default: None

Padding from the right edge to position the text.

---

> top = Type: Int | Default: None

Padding from the top edge to position the text.

---

> bottom = Type: Int | Default: None

Padding from the bottom edge to position the text.

---

You only need to set `left` or `right`, not both.

You only need to set `top` or `bottom`, not both.

If those are not set then the text is placed at the center.

---

> width = Type: Int | Default: None

Fixed width to every frame. Height is always automatic.

---

> input = Type: Str | Default: media/video.webm

Which video or image to use for the frames.

`-i` is a shorter alias for this.

---

> output = Type: Str | Default: 'output' directory

In which directoy to save the generated gif.

`-o` is a shorter alias for this.

---

> words = Type: Str | Default: No words

The words string to use. Lines are separated by `;`.

---

> format = Type: Str | Default: "gif"

The format of the output file. Either `gif` or `mp4`.

This is only used when the output is not a direct file path.

For instance if the output ends with `cat.gif` it will use `gif`.

If the output is a directory it will use a random name with the appropiate format.

---

> separator = Type: Str | Default: ";"

Which character to consider as the separator in `words`.

---

> order = Type: Str | Default: "random"

The order used to extract the frames.

Either `random` or `normal`.

`random` picks frames randomly.

`normal` picks frames in order starting from the first one.

`normal` loops back to the first frame if needed.

---

> font = Type: Str | Default "simple"

The font to use for the text.

Either `simple`, `complex`, `plain`, `duplex`, or `triplex`.

---

> fontsize = Type: Int | Default: 3

The size of the text.

---

> fontcolor = Type: Str | Default: "255,255,255"

The color of the text.

3 numbers from 0 to 255, separated by commas.

`0,0,0` would be black for instance.

> boldness = Type: Float | Default: 3

The thickness of the text.

---

<img src="media/borat.gif" width="600">