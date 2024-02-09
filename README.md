<img src="media/borat.jpg" width="350">

This is a python program to produce gif images.

It extracts random frames from a video.

It (optionally) places words somewhere on each frame.

Then joins all frames into an animated gif.

## Why?

It might be useful in the realm of human verification.

And memes.

## Installation

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

## Usage

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
venv/bin/python src/borat.py --video="/videos/stuff.webm" --size=3 --thick=3 --fps=1.5 --width=600 --words="; I want to eat;; [Random]"
```

You can run `borat.py` from anywhere in your system using its virtual env. Relative paths should work fine.

## Defaults

It uses these defaults (defined in `state.py`):

```
fps = 2.2
frames = 3
size = 3
thick = 3
left = None
right = None
top = None
bottom = None
width = None
```

---

All of these can be set with flags like `--fps=3 --top=0 --width=500`

---

`fps` (frames per second) modifies the speed between frame change (ms).

A bigger `fps` = A faster gif.

`frames` is the amount of frames to use if `--words` is not used.

`left` is the padding from the left edge.

`right` is the padding from the right edge.

`top` is the padding from the top edge.

`bottom` is the padding from the bottom edge.

You only need to set `left` or `right`, not both.

You only need to set `top` or `bottom`, not both.

If these are not set then the text is placed at the center.

`size` and `thick` modify the text's size and thickness.

`width` sets a fixed width to every frame. Height is always automatic.

---

<img src="media/borat.gif" width="600">