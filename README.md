# About

This repo keeps track of which [Destiny](https://www.youtube.com/user/destiny) VODs are currently transcribed for [knowyourinfluencer.io](https://knowyourinfluencer.io/destiny/)

## How to contribute

You can contribute to this project by using `Whisperer.py` and generating a transcript for a video that has not yet been transcribed. All un-transcribed videos have a [deidcated issue](https://github.com/Ethan0429/destiny-transcript-db/issues). The steps are simple:

1. Comment under an issue you wish to claim
2. Complete the transcription process described in the [How to transcribe](#how-to-transcribe) section below.
3. Submit a pull request with the transcript csv file in the `transcripts/` directory, addressing the issue you claimed.

## How to transcribe

I've made the process as streamlined as I could. All you need is a little programming experience, a GitHub account, and of course the dependencies/hardware requirements needed to run `Whisperer.py`.

### Alternative to dependencies: Docker & Docker Compose

If you rather not install the dependencies and are familiar with Docker, you can use the Dockerfile provided instead. Otherwise, go to [the requirements section](###requirements).

Firstly, download the `vosk` model. You can see the instructions for that [here](#vosk-model).

Assuming you have Docker & Docker Compose installed, simply fork this repo, and build & run the container with

```bash
# template example
VIDEO_ID=<video_id> docker-compose up

# real example
VIDEO_ID=6zK3i3uK-E0 docker-compose up
```

### Alternative to dependencies: Poetry

You can also use [Poetry](https://python-poetry.org/) to install the dependencies. This is the recommended method if you're on MacOS or Linux.

Knock these two things out of the way first:

1. First and foremost, I download `ffmpeg` for your system. You can see the instructions for that [here](#ffmpeg).

2. Download the `vosk` model. You can see the instructions for that [here](#vosk-model).

Now you can install the dependencies and run `Whisperer.py` with Poetry.

#### Install dependencies

```bash
poetry install
```

If `vosk` doesn't successfully install, run the following command instead:

```bash
poetry run pip3 install vosk
```

#### Run `Whisperer.py`

```bash
poetry run python3 Whisperer.py <video_id>
```

### Requirements

There are 4 requirements for this project.

- Python 3.7 or greater
- `ffmpeg`
- `vosk`
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

#### vosk

```bash
pip3 install vosk
```

#### vosk model

Download this model https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip (**it must be this one exactly**) and extract it to it to a `model/` directory in the root of this repo.

The directory structure should look something like this:

```
model
├── am
│  ├── final.mdl
│  └── tree
├── conf
│  ├── ivector.conf
│  ├── mfcc.conf
│  └── model.conf
├── graph
│  ├── disambig_tid.int
│  ├── HCLG.fst
│  ├── num_pdfs
│  ├── phones
│  │  ├── align_lexicon.int
│  │  ├── align_lexicon.txt
│  │  ├── disambig.int
│  │  ├── disambig.txt
│  │  ├── optional_silence.csl
│  │  ├── optional_silence.int
│  │  ├── optional_silence.txt
│  │  ├── silence.csl
│  │  ├── word_boundary.int
│  │  └── word_boundary.txt
│  ├── phones.txt
│  └── words.txt
├── ivector
│  ├── final.dubm
│  ├── final.ie
│  ├── final.mat
│  ├── global_cmvn.stats
│  ├── online_cmvn.conf
│  └── splice.conf
```

#### youtube-dl

I recommend installing `yt-dlp` with `pip`, which you can do with

```bash
python3 -m pip install -U yt-dlp
```

#### forking the repo

You'll need to fork the repo so you can later submit a pull request once you've generated a transcript. You can do this by clicking the "Fork" button in the top right corner of the repo page, and cloning it to your machine where you'll be running `Whisperer.py`.

### Running `Whisperer.py`

Once you've claimed an issue, the `video_id` you'll be generating a transcribt for is **the title of that issue itself**. You'll use this when running `Whisperer.py`.

`Whisperer.py` will download whatever video you provide, generate the transcript, and output it as `<video_id>.csv` in the `transcripts/` directory. It *requires* 1 argument, and takes 1 optional argument.

```
usage: whisperer.py [-h] [--model MODEL] video_id

positional arguments:
  video_id       The Video ID of the YouTube video being transcribed, e.g. "NyiJDDyUV54"

options:
  -h, --help     show this help message and exit
```

#### Example

```bash
python3 whisperer.py NyiJDDyUV54
```

#### Submitting a pull request

Once it's run, it will take quite awile to finish depending on the size of the video, so just leave it running in the background for awhile. When it's finished, commit your changes to your repo with a message `resolves #xxx`, push it to GitHub, and submit a pull request for the corresponding issue you claimed.

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

## Transcribing Odysee Videos

`Whisperer.py` also allows you to transcribe Odysee videos. The process is the same as YouTube videos, except instead of passing a YouTube video ID, you pass the entire Odysee URL.

#### Example

```bash
python3 Whisperer.py https://odysee.com/@gnomevods:3/RSIejcoWqCU:a
```

## End

If/when your pull request is approved and merged, I'll update the database to include it, and I'll list you as a contributor at https://knowyourinfluencer.io/contributors/.

Thanks for your help. dggL
