# About

This repo keeps track of which [Destiny](https://www.youtube.com/user/destiny) VODs are currently transcribed for [knowyourinfluencer.io](https://knowyourinfluencer.io/destiny/)

## How to contribute

You can contribute to this project by using `Whisperer.py` and generating a transcript for a video that has not yet been transcribed. All un-transcribed videos have a [deidcated issue](https://github.com/Ethan0429/destiny-transcript-db/issues). The steps are simple:

1. Comment under an issue you wish to claim
2. Complete the transcription process described in the [How to transcribe](#how-to-transcribe) section below.
3. Submit a pull request with the transcript csv file in the `transcripts/` directory, addressing the issue you claimed.

## How to transcribe

I've made the process as streamlined as I could. All you need is a little programming experience, a GitHub account, and of course the dependencies/hardware requirements needed to run `Whisperer.py`.

## Requirements

The only way I've provided to generate a transcript is through Docker & docker-compose.

- [Docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

It is possible without Docker, but making it portable is not a simple task, so I've opted to use Docker for the distribution.

### Forking The Repo

You'll need a GitHub account and `git` installed on your machine for this part.

You'll need to fork the repo so you can later submit a pull request once you've generated a transcript. You can do this by clicking the "Fork" button in the top right corner of the repo page, and cloning it to your machine where you'll be running `Whisperer.py`.

## Running `Whisperer.py`

Once you've claimed an issue, the `video_id` you'll be generating a transcript for is **the title of that issue itself**. You'll then use it with `docker-compose` to generate a transcript.


#### Example

```bash
# template example
VIDEO_ID=<video_id> docker-compose up

# real example
VIDEO_ID=6zK3i3uK-E0 docker-compose up
```

This will build the Docker image, start the container, and run `Whisperer.py` with the provided `VIDEO_ID`. It will output the transcript as `transcripts/<video_id>.csv`. You can then submit a pull request with the transcript.

## Submitting a pull request

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
VIDEO_ID=https://odysee.com/@gnomevods:3/RSIejcoWqCU:a docker-compose up
```

## End

If/when your pull request is approved and merged, I'll update the database to include it, and I'll list you as a contributor at https://knowyourinfluencer.io/contributors/.

Thanks for your help. dggL
