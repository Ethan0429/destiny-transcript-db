import argparse
import csv
import json
import os
import sys
import json
import subprocess as sp
from vosk import Model, KaldiRecognizer, SetLogLevel
import yt_dlp

SAMPLE_RATE = 16000
SetLogLevel(-1)


class Whisperer:
    def __init__(self, video_id: str = None, date: int = None):
        self.model = Model(lang="en-us")
        self.video_id = video_id
        self.segments = []
        self.date = date if date is not None else 20230101

    def transcribe(self):
        self.segments = self.__coalesce_segments()
        return self.segments

    def __coalesce_segments(self):
        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        rec.SetWords(True)
        segments = []
        with sp.Popen(["ffmpeg", "-loglevel", "quiet", "-i", "audio.m4a", "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"], stdout=sp.PIPE) as process:

            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    part_result = json.loads(rec.Result())
                    segments.append(part_result)

            part_result = json.loads(rec.FinalResult())
            segments.append(part_result)

        results = []
        for i in segments:
            # check if result key exists
            if 'result' not in i:
                continue
            for result in i['result']:
                results.append(result)

        coalesced_results = []
        for result in results:
            if result['word'] == '':
                continue

            start_time = float(result['start'])
            end_time = result['end']
            new_result = {}
            new_result['word'] = result['word']
            new_result['start'] = start_time
            skip = 1

            try:
                # add the next result to the current result if the next result is within 20 seconds or the current result is less than 40 words
                while (float(results[results.index(result) + skip]['start']) - start_time) < 20.0 and len(result['word'].split()) < 40:
                    new_result['word'] += ' ' + \
                        results[results.index(result) + skip]['word']
                    results[results.index(result) + skip]['word'] = ''
                    skip += 1
            except IndexError:
                pass

            coalesced_results.append(new_result)
        return coalesced_results

    def write_to_csv(self):
        with open(f'./transcripts/{self.video_id}.csv', 'w') as f:
            # write header
            f.write('video_id,date,start,text\n')

            # remove all segments that are less than 5 words
            self.segments = list(
                filter(lambda segment: len(segment['word'].split()) > 5, self.segments))

            # write segments
            for segment in self.segments:
                f.write(
                    f'{self.video_id},{self.date},{int(segment["start"])},{segment["word"].strip()}\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id', help='The Video ID of the YouTube video being transcribed, e.g. "NyiJDDyUV54"',
                        type=str)
    return parser.parse_args()


def extract_date(title: str):
    try:
        title = title.replace('(', '').replace(')', '')
        year, month, day = title.split('-', 2)

        # remove any leading zeros
        if year[0] == '0':
            year = year[1:]
        if month[0] == '0':
            month = month[1:]
        if day[0] == '0':
            day = day[1:]

        try:
            int(day[0:2])
            day = day[0:2]
        except ValueError:
            day = day[0]

        if len(day) == 1:
            day = '0' + day

        if len(month) == 1:
            month = '0' + month

        date = int(year + month + day)
    except:
        date = None

    return date


def main():
    args = parse_args()

    URLS = [
        f'https://www.youtube.com/watch?v={args.video_id}'] if 'odysee' not in args.video_id else [f'{args.video_id}']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'audio.m4a',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(URLS[0], download=True)
        video_title = info_dict.get('title', None)

    video_id = args.video_id.split(
        '/')[-1] if 'odysee' in args.video_id else args.video_id

    # create whisperer
    whisperer = Whisperer(video_id=video_id, date=extract_date(
        video_title))
    # transcribe
    segments = whisperer.transcribe()
    whisperer.write_to_csv()


if __name__ == '__main__':
    exit(main())
