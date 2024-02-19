<img src="media/image.jpg" width="380">

This is a Python program to produce gif images or videos.

It extracts random (or sequential) frames from a video or image.

It (optionally) places words somewhere on each frame.

Then joins all frames into an animated `gif` or `mp4`.

You can use many arguments to produce different kinds of animations.

---

## Why?

It might be useful in the realm of human verification.

<img src="media/mean.gif">

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

```shell
git clone --depth 1 this_repo_url

cd new_directory
```

Then create the virtual env:

```shell
python -m venv venv
```

Then install the dependencies:

```shell
venv/bin/pip install -r requirements.txt
```

Or simply run `scripts/install.sh` to create the virtual env and install the dependencies.

There's a `scripts/test.sh` file that runs the program with some arguments to test if things are working properly.

---

<img src="media/usage.gif">

---

## Usage <a name="usage"></a>

Run `src/main.py` using the Python in the virtual env:

```shell
venv/bin/python src/main.py
```

You can provide a video or image path using the `--input` argument:

```shell
venv/bin/python src/main.py --input "/path/to/video.webm"
venv/bin/python src/main.py --input "/path/to/animated.gif"
venv/bin/python src/main.py --input "/path/to/image.png"
```

`webm`, `mp4`, `gif`, `jpg`, and `png` should work, and maybe other formats.

You can pass it a string of lines to use on each frame.

They are separated by `;` (semicolons).

```shell
venv/bin/python src/main.py --words "Hello Brother ; Construct Additional Pylons"
```

It will make 2 frames, one per line.

If you want to use words and have some frames without them simply use more `;`.

---

You can use random words with `[random]`:

```shell
venv/bin/python src/main.py --words "I Like [random] and [random]"
```

It will pick random words from a list of English words.

There are 3 kinds of random formats: `[random]`, `[RANDOM]`, and `[Random]`.

The replaced word will use the case of those.

For example `[RANDOM]` might be `PLANET`.

You can specify how many random words to generate by using a number:

For example `[Random 3]` might generate `Drivers Say Stories`.

---

You can multiply random commands by using numbers like `[x2]`.

For example:

```
--words "Buy [Random] [x2]"
```

This might produce: `Buy Sink ; Buy Plane`.

The multipliers need to be at the end of the line.

---

You can also generate random numbers with `[number]`.

For example, `[number]` might result in `3`.

You can specify the length of the number.

For example, `[number 2]` might result in `28`.

---

`[random]` and `[number]` can use a range.

For example, `[number 1-3]` will pick a random length between `1` and `3`.

For example, it could be `88` if it resulted in `2` (Length of 2).

Same with `[random 2-3]`.

---

If you want to repeat the previous line, use `[repeat]`:

For example: `--words "Buy Buttcoin ; [repeat]"`.

It will use that text in the first two frames.

You can also provide a number to specify how many times to repeat:

For example: `--words "Buy Buttcoin ; [repeat 2]"`.

The line will be shown in 3 frames (the original plus the 2 repeats).

---

You can use linebreaks with `\n`.

For example: `--words "Hello \n World"`.

Will place `Hello` where a normal line would be.

And then place `World` underneath it.

You can control the spacing with the `linespace` argument.

---

Another way to define an empty line is using `[empty]`.

For example: `hello ; world ; [empty]`.

This could be useful in `wordfile` to add empty lines at the end.

Else you can just add more `;` to `words`.

You can also use numbers like `[empty 3]`.

That would add 3 empty frames.

---

You can run `main.py` from anywhere in your system using its virtual env.

Relative paths should work fine.

---

Here's a fuller example:

```shell
venv/bin/python src/main.py --input "/videos/stuff.webm" --fontsize 2.8 --delay 300 --width 600 --words "I want to eat ;; [Random] ; [repeat 2] ;" --format mp4 --bgcolor 0,0,0 --baseline --output "stuff/videos"
```

---

<img src="media/arguments.gif">

---

## Arguments <a name="arguments"></a>

You can use arguments like: `--delay 350 --width 500 --order normal`.

These modify how the file is going to be generated.

---

> **input** (Type: str | Default: The included video)

Path to a video or image to use as the source of the frames.

`webm`, `mp4`, `gif`, and even `jpg` or `png` should work.

For example: `--input stuff/cow.mp4`.

It's possible to use multiple input files by separating them with commas.

For example: `--input /some/path/1.gif,/some/other/path/2.mp4,/another/one/3.png`.

If multiple inputs, one is selected randomly as the source of the frames.

`-i` is a shorter alias for this.

---

> **output** (Type: str | Default: The output directory)

Directory path to save the generated file.

For example: `stuff/videos`.

It will use a random file name.

Using `gif` or `mp4` depending on the `format` argument.

Or you can enter the path plus the file name.

For example: `stuff/videos/cat.gif`.

The format is deduced by the extension (`gif` or `mp4`).

`-o` is a shorter alias for this.

---

> **words** (Type: str | Default: Empty)

The words string to use.

Lines are separated by `;`.

Each line is a frame.

Special words include `[random]` and `[repeat]`.

As described in [Usage](#usage).

---

> **wordfile** (Type: str | Default: None)

File to use as the source of word lines.

For example, a file can be like:

```
This is a line
I am a [random]

This is a line after an empty line
[repeat]
[empty]
```

Then you can point to it like:

```
--wordfile "/path/to/words.txt"
```

It will use word lines the same as with `--words`.

---

> **fillwords** (Type: flag | Default: False)

Fill the rest of the frames with the last word line.

If there are no more lines to use, it will re-use the last line.

You can do like:

```
--words "Single Line" --frames 5 --fillwords
```

And it will use that line in all 5 frames.

---

> **separator** (Type: str | Default: ";")

The character to use as the line separator in `words`.

This also affects `randomlist`.

---

> **linebreak** (Type: str | Default: "\n")

The character to use for linebreaks.

---

> **linespace** (Type: int | Default 20)

Spacing between lines separated by `\n`.

---

> **delay** (Type: int | Default: 600)

The delay between frames. In milliseconds.

A smaller `delay` = A faster animation.

---

> **frames** (Type: int | Default: 3)

The amount of frames to use.

This value has a higher priority than the other frame count methods.

---

> **framelist** (Type: str | Default: Empty)

The specific list of frame indices to use.

The first frame starts at `0`.

For example `--framelist "2,5,2,0,3"`.

It will use those specific frames.

It also defines how long the animation is.

---

> **left** (Type: int | Default: None)

Padding from the left edge to position the text.

---

> **right** (Type: int | Default: None)

Padding from the right edge to position the text.

---

> **top** (Type: int | Default: None)

Padding from the top edge to position the text.

---

> **bottom** (Type: int | Default: None)

Padding from the bottom edge to position the text.

---

You only need to set `left` or `right`, not both.

You only need to set `top` or `bottom`, not both.

If those are not set then the text is placed at the center.

If any of those is set to a negative value like `-100`, it will apply it from the center.

For example: `--top -100` would pull it a bit to the top from the center.

And `--right -100` would pull it a bit to the right from the center.

---

> **width** (Type: int | Default: None)

Fixed width to every frame. Height is always automatic.

---

> **format** (Type: str | Default: "gif")

The format of the output file. Either `gif` or `mp4`.

This is only used when the output is not a direct file path.

For instance, if the output ends with `cat.gif` it will use `gif`.

If the output is a directory it will use a random name with the appropriate format.

---

> **order** (Type: str | Default: "random")

The order used to extract the frames.

Either `random` or `normal`.

`random` picks frames randomly.

`normal` picks frames in order starting from the first one.

`normal` loops back to the first frame if needed.

---

> **font** (Type: str | Default "simple")

The font to use for the text.

Either `simple`, `complex`, `plain`, `duplex`, or `triplex`.

---

> **fontsize** (Type: float | Default: 2.5)

The size of the text.

The number acts as a scale, not exact pixels.

---

> **fontcolor** (Type: str | Default: "255,255,255")

The color of the text.

3 numbers from `0` to `255`, separated by commas.

`0,0,0` would be black, for instance.

It uses the `RGB` format.

The value can also be `random_light` or `random_dark`.

These will get a random light or dark color.

The value can also be `random_light2` or `random_dark2`.

These will get a random light or dark color on each frame.

---

> **boldness** (Type: int | Default: 3)

The thickness of the text.

The bigger the number, the fatter the text is.

---

> **bgcolor** (Type: str | Default: None)

Add a background rectangle below the text.

In case you want to give the text more contrast.

3 numbers from `0` to `255`, separated by commas.

`0,0,0` would be black, for instance.

It uses the `RGB` format.

The value can also be `random_light` or `random_dark`.

These will get a random light or dark color.

The value can also be `random_light2` or `random_dark2`.

These will get a random light or dark color on each frame.

---

> **opacity** (Type: float | Default: 0.5)

From `0` to `1`.

The opacity level of the background rectangle.

The closer it is to `0` the more transparent it is.

---

> **padding** (Type: int | Default: 25)

The padding of the background rectangle.

This gives some spacing around the text.

This also sets the margin for `left`, `right`, `top`, and `bottom`.

---

> **baseline** (Type: flag | Default: False)

Use this to add the baseline to the background rectangle's height.

The baseline is the room reserved for letters that have descenders, like the bottom half of `y`.

If you enable it the rectangle will cover all possible letters.

---

> **randomlist** (Type: str | Default: Empty)

Random words are selected from this list.

If the list is empty it will be filled with a long list of nouns.

You can specify the words to consider, separated by semicolons.

For example: `--randomlist "cat ; dog ; nice cow ; big horse"`.

---

> **randomfile** (Type: str | Default: List of nouns)

Path to a text file with the random words to use.

This is a simple text file with each word or phrase in its own line.

For example:

```
dog
a cow
horse
```

Then you point to it: `--randomfile "/path/to/animals.txt"`.

---

> **repeatrandom** (Type: flag | Default: False)

If this is enabled, random words can be repeated at any time.

Else it will cycle through them randomly without repetitions.

---

> **loop** (Type: int | Default 0)

How to loop gif renders.

`-1` = No loop

`0` = Infinite loop

`1 or more` = Specific number of loops

---

> **filter** (Type: str | Default: "none")

A color filter that is applied to each frame.

The filters are: `hue1`, `hue2` .. up to `hue8`, and `anyhue`, `anyhue2`.

And also: `gray`, `blur`, `invert`, `saturate`, `random`, `random2`, `none`.

`random` picks a random filter for all frames.

`random2` picks a random filter on every frame.

`anyhue` is like `random` but limited to the hue effects.

`anyhue2` is like `random2` but is limited to the hue effects.

---

> **filteropts** (Type: str | Default: Empty)

This defines the pool of available filters to pick randomly.

This applies when `filter` is `random` or `random2`.

For example: `--filteropts "hue1,hue2,hue3,gray"`.

---

> **repeatfilter** (Type: flag | Default: False)

If this is enabled, random filters can be repeated at any time.

Else it will cycle through them randomly without repetitions.

---

> **remake** (Type: flag | Default: False)

Use this if you only want to re-render the frames.

It re-uses all the frames, resizes, and renders again.

It doesn't do the rest of the operations.

For example: `--input "/path/to/file.gif" --remake --width 500 --delay 300`.

For instance, you can use this to change the `width` or `delay` of a rendered file.

---

### Scripts

You can make `TOML` files that define the arguments to use.

Provide the path of a script like this: `--script "/path/to/script.toml"`.

For example, a script can look like this:

```toml
words = "Disregard [Random] ; [repeat] ; Acquire [Random] ; [repeat] ;"
fontcolor = "44,80,200"
bgcolor = "0,0,0"
bottom = 0
right = 0
```

---

### Functions

You can write shell functions to make things faster by using templates.

For example here's a `fish` function:

```js
function funstuff
	/path/to/venv/bin/python /path/to/gifmaker/src/main.py \
	--input "/path/to/some/file.png" --words "$argv is [Random] [x5]" \
	--bgcolor random_dark2 --fontcolor random_light2 \
	--top 0 --fontsize 2.3 --filter random2 --width 600
end
```

This is added in `~/.config/fish/config.fish`.

Source the config after adding the function:

```shell
source ~/.config/fish/config.fish
```

Then you can run: `funstuff Grog`.

In this case it will do `Grogg is [Random]` 5 times.

Using all the other arguments that are specific to look good on that image.