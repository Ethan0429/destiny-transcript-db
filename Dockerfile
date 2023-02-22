FROM golang:1.19.6-bullseye

ENV KYI_CONTAINERIZED=1

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg git unzip wget

RUN apt-get install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install internetarchive && \
    pip3 install python-dotenv && \
    pip3 install vosk && \
    pip3 install typesense && \
    pip3 install rich && \
    pip3 install yt-dlp

WORKDIR /destiny-transcript-db

RUN mkdir -p /destiny-transcript-db/model && \
    wget https://alphacephei.com/vosk/models/vosk-model-en-us-daanzu-20200905.zip && \
    unzip *.zip && \
    cp -r /destiny-transcript-db/vosk-model-en-us-daanzu-20200905/* /destiny-transcript-db/model && \
    rm -rf vosk-model-en-us-daanzu-20200905 && \
    rm *.zip

COPY . .

RUN chmod +x ./transcribe.sh

ENTRYPOINT [ "python3", "-u", "Whisperer.py" ]