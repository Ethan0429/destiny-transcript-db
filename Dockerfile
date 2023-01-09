FROM python:3.10-bullseye

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg git

RUN pip install git+https://github.com/openai/whisper.git
RUN pip install yt-dlp

WORKDIR /destiny-transcript-db

ARG video_id
ARG model=base
ENV video_id ${video_id}
ENV model ${model}

# Copy the current directory contents into the container at /app
COPY . /destiny-transcript-db

CMD python3 Whisperer.py ${video_id} --model ${model}