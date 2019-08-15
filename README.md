# YTSound: Extract audio from youtube video to .mp3 file

## Requirements:
* Python 2.7 (not tested in Python 3.x)
* `lame` and `ffmpeg`, 
* `pytube`: already included in this source, fixed many bugs that prevent downloading video

If the libraries are not installed just run the following command in your terminal:
* **On Mac (OS X)**: `brew install lame ffmpeg`
* **On Linux (Ubuntu)**: `sudo apt-get install lame ffmpeg`

## How to use it:
Syntax command:
```
python ytsound.py [-o <output path>] link [link...]
```

**Options**
* `output path`: where to save .mp3 files. Default is `audio` sub-directory in current working directory
* `link`: you can specify as many links as you want, but at least 1