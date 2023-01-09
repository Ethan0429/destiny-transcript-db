# About

This repo keeps track of which [Destiny](https://www.youtube.com/user/destiny) VODs are currently transcribed for [knowyourinfluencer.io](https://knowyourinfluencer.io/destiny/)

## How to contribute

You can contribute to this project by using `Whisperer.py` and generating a transcript for a video that has not yet been transcribed. All un-transcribed videos have a [deidcated issue](https://github.com/Ethan0429/destiny-transcript-db/issues). The steps are simple:

1. Comment under an issue you wish to claim
2. Complete the transcription process described in the [How to transcribe](#how-to-transcribe) section below.
3. Submit a pull request with the transcript csv file in the `transcripts/` directory, addressing the issue you claimed.

## How to transcribe

I've made the process as streamlined as I could. All you need is a little programming experience, a GitHub account, and of course the dependencies/hardware requirements needed to run `Whisperer.py`.

### Requirements

There are 4 requirements for this project.

- Python 3.7 or greater
- `ffmpeg`
- `whisper`
- `yt-dlp`

#### ffmpeg

You can install `ffmpeg` using your package manager of choice. (I recommend using a package manager, but you can install from https://ffmpeg.org/download.html instead)

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

#### whisper

[Install whisper](https://github.com/openai/whisper#setup)

#### youtube-dl

I recommend installing `yt-dlp` with `pip`, which you can do with

```bash
python3 -m pip install -U yt-dlp
```

#### forking the repo

You'll need to fork the repo so you can later submit a pull request once you've generated a transcript. You can do this by clicking the "Fork" button in the top right corner of the repo page, and cloning it to your machine where you'll be running `Whisperer.py`.

### Running `Whisperer.py`

`Whisperer.py` will download whatever video you provide, generate the transcript, and output it as `<video_id>.csv` in the `transcripts/` directory. It *requires* 1 argument, and takes 1 optional argument.

```
usage: whisperer.py [-h] [--model MODEL] video_id

positional arguments:
  video_id       The Video ID of the YouTube video being transcribed, e.g. "NyiJDDyUV54"

options:
  -h, --help     show this help message and exit
  --model MODEL  The Whisper model being used, e.g. "base" or "large". Depends on your hardware. See https://github.com/openai/whisper#available-models-and-languages to see which models your system can
                 run. Default is "base".
```

`--model` is `base` by default, but depending on your machine's VRAM you can (and probably should) use a larger model. 

**Make sure you're using the right model for your machine, since using a model that's too large for your machine will cause `Whisperer.py` to crash.**

More info on the model types and hardware requirements can be found [here](https://github.com/openai/whisper#available-models-and-languages)

#### Example

```bash
# using base whisper model
python3 whisperer.py NyiJDDyUV54

# using large whisper model
python3 whisperer.py NyiJDDyUV54 --model large
```

#### Submitting a pull request

Once it's run, it will take quite awile to finish depending on the size of the video, so just leave it running in the background for awhile. When it's finished, commit your changes to your repo, push it to GitHub, and submit a pull request for the corresponding issue you claimed.

Your pull request should be in the following format:

```
title: resolves <video_id_issue_number>
description: How you want to be listed as a contributor (e.g. what image, name/username), and any notes you have about the transcript.
```

For example, the following pull request address issue #256
#### Example

```
title: resolves #256
description: Username: EvilFossil, image: https://i.kym-cdn.com/entries/icons/original/000/025/526/gnome.jpg
```

## End

If/when your pull request is approved and merged, I'll update the database to include it, and I'll list you as a contributor at https://knowyourinfluencer.io/contributors/.

Thanks for your help. dggL
