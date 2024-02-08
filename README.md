<img src="borat.jpg" width="350">

This uses a video to extract x number of random frames.

It places random words somewhere on the frames.

Then joins all frames into a gif.

## Installation

Clone this repo, and get inside the dir.

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

## Why?

It might become useful eventually.

Maybe in the realm of human verification.

Plus it's kinda funny.