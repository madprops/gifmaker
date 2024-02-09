<img src="media/borat.jpg" width="350">

This is a python program to produce gif images.

It extracts random frames from a video.

It (optionally) places words somewhere on each frame.

Then joins all frames into an animated gif (or mp4).

## Why?

It might be useful in the realm of human verification.

And memes.

## Index
1. [Installation](#installation)
1. [Usage](#usage)
1. [Arguments](#arguments)

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

## Usage <a name="usage"></a>

Run `src/borat.py` using the python in the virtual env:

```
venv/bin/python src/borat.py
```

You can provide any video path using the `--video` flag:

```
venv/bin/python src/borat.py --video="/path/to/video.webm"
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
venv/bin/python src/borat.py --video="/videos/stuff.webm" --size=3 --thick=3 --fps=1.5 --width=600 --words="; I want to eat;; [Random] --ext="mp4"
```

You can run `borat.py` from anywhere in your system using its virtual env. Relative paths should work fine.

## Arguments <a name="arguments"></a>

You can use flag arguments like: `--fps=3 --top=0 --width=500`

These modify how the gif image is going to be generated.

---

> fps = Type: Float | Default: 2.2

(Frames Per Second) modifies the speed between frame change (ms).

A bigger `fps` = A faster gif.

---

> frames = Type: Int | Default: 3

The amount of frames to use if `--words` is not used.

---

> size = Type: Int | Default: 3

The size of the text.

---

> thick = Type: Float | Default: 3

The thickness of the text.

---

> left = Type: Int | Default: None

Padding from the left edge.

---

> right = Type: Int | Default: None

Padding from the right edge.

---

> top = Type: Int | Default: None

Padding from the top edge.

---

> bottom = Type: Int | Default: None

Padding from the bottom edge.

---

You only need to set `left` or `right`, not both.

You only need to set `top` or `bottom`, not both.

If those are not set then the text is placed at the center.

---

> width = Type: Int | Default: None

Fixed width to every frame. Height is always automatic.

---

> outdir = Type: Str | Default: 'output' directory

In which directoy to save the generated gif.

---

> video = Type: Str | Default: 'media/video.webm'

Which video to use for the frames.

---

> words = Type: Str | Default: No words

The words string to use. Lines are separated by `;`.

---

> ext = Type: Str | Default: gif

The format of the output file. Either `gif` or `mp4`.

---

<img src="media/borat.gif" width="600">