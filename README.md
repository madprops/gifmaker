<img src="borat.jpg" width="350">

This uses a video to extract x number of random frames.

It places a word somewhere on each frame.

Then joins all frames into a gif.

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

You can supply a string as an argument:

```
venv/bin/python borat.py "Construct Additional Pylons"
```

In this case each word is a frame, so 3 frames.

Or let it pick some random words (3 by default):

```
venv/bin/python borat.py
```

You can also define the number of random words to use:

```
venv/bin/python borat.py 5
```

## Defaults

It's fine-tuned to work with the provided video.

It uses these defaults (defined in `borat.py`):

```
FPS = 2.2
RIGHT = 45
BOTTOM = 100
SCALE = 3
THICK = 3
```

`FPS` (frames per second) modifies the speed between frame change (ms).

`RIGHT` is the padding from the right edge.

`BOTTOM` is the padding from the bottom.

A bigger `FPS` = A faster gif.

`SCALE` and `THICK` modify the text's size and thickness.

If you want to use a different video, you might need to adjust these.

Also name the video file `video.webm` or modfiy the `VIDEO` value in `borat.py`.

## Why?

It might become useful eventually.

Maybe in the realm of human verification.

Plus it's kinda funny.