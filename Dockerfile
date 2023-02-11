FROM python:3.10-bullseye

ENV KYI_CONTAINERIZED=1

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg git

RUN pip install vosk && \
    pip install yt-dlp

WORKDIR /destiny-transcript-db

# Copy the current directory contents into the container at /app
COPY . /destiny-transcript-db

ENTRYPOINT [ "python3", "Whisperer.py" ]