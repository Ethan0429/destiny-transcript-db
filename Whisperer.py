'''
#####################################################################################
#####################################################################################
############ /Whisperer.py & /stream-archiver/Whisperer.py are symlinked ############
#####################################################################################
#####################################################################################
'''

import wave
import argparse
import csv
import time
import logging
import json
import os
import sys
import json
import subprocess as sp
from dotenv import load_dotenv
from vosk import Model, KaldiRecognizer, SetLogLevel
from rich import print_json
from rich.progress import track, Progress
from rich.console import Console
from rich.theme import Theme
from rich import print
from rich.traceback import install
from multiprocessing import Pool as ThreadPool
install()
load_dotenv()

SAMPLE_RATE = 16000
FRAME_SIZE = int(os.getenv('FRAME_SIZE'))
SetLogLevel(-1)

model = Model("model")


def concatentate_segment_times(data: list):
    prev_start = 0.0
    increment = 0.0
    # Iterate through each result array
    for results in data:
        if 'result' not in results:
            continue
        # Iterate through each result object in the array
        for result in results['result']:
            # if the current start time is less than the previous start time, update increment to the last end time
            if result['start'] < prev_start:
                increment += float(FRAME_SIZE)

            prev_start = result['start']

            # update the start time to the current start time plus the increment
            result['start'] += increment
            result['end'] += increment

    return data


class Whisperer:

    def __init__(self, video_id: str = None, date: int = None, audio_file: str = 'pre-audio.wav', model: str = 'model'):
        self.video_id = video_id
        self.segments = []
        self.date = date if date is not None else 20230101
        self.audio_file = audio_file
        self.console = Console(theme=Theme({
            'log': 'bold cyan',
            'success': 'bold green',
            'error': 'bold red'
        }))
        self.console.log(
            f"Initialized Whisperer for {self.video_id}", log_locals=True, style="log")

    def transcribe(self):
        self.__extract_audio()

        self.console.log(
            f"🔉 Transcribing {self.audio_file}...", style="log")

        # transcribe each audio file
        sp.run(["./transcribe.sh"], check=True, shell=True)

        # load the transcription data
        with open('transcription.json', 'r') as f:
            self.segments = json.load(f)

        self.segments = concatentate_segment_times(self.segments)

        self.console.log('✅ Audio transcribed', style='success')
        self.segments = self.__coalesce_segments()

    def __extract_audio(self):
        with self.console.status("🔊 [bold cyan]Extracting audio...", spinner='aesthetic') as status:
            sp.run(["ffmpeg", "-loglevel", "quiet", "-i", self.audio_file, "-ac",
                    "1", "-ar", str(SAMPLE_RATE), 'audio.wav'], check=True)

        self.audio_file = 'audio.wav'
        self.console.log('✅ Audio extracted', style='success')

    def __coalesce_segments(self):
        results = []
        for i in self.segments:
            # check if result key exists
            if 'result' not in i:
                continue
            for result in i['result']:
                results.append(result)

        coalesced_results = []
        for result in track(results, description="[bold cyan]Coalescing results...", show_speed=True, total=len(results)):
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
                while (float(results[results.index(result) + skip]['start']) - start_time) < 20.0 and len(new_result['word'].split()) < 40:
                    new_result['word'] += ' ' + \
                        results[results.index(result) + skip]['word']
                    results[results.index(result) + skip]['word'] = ''
                    skip += 1
            except IndexError:
                pass

            coalesced_results.append(new_result)

        return coalesced_results

    def write_to_csv(self, path: str = './transcripts'):
        filename = self.video_id.split(
            'kyi-')[1] if 'kyi-' in self.video_id else self.video_id

        with open(f'{path}/{filename}.csv', 'w') as f:
            # write header
            f.write('video_id,date,start,text\n')

            # remove all segments that are less than 5 words
            self.segments = list(
                filter(lambda segment: len(segment['word'].split()) > 5, self.segments))

            # write segments
            for segment in track(self.segments, description="[bold cyan]Writing to CSV...", show_speed=True, total=len(self.segments)):
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
            int(day[0: 2])
            day = day[0: 2]
        except ValueError:
            day = day[0]

        if len(day) == 1:
            day = '0' + day

        if len(month) == 1:
            month = '0' + month

        date = int(year + month + day)
    except:
        print('[bold red]Could not extract date from title!')
        date = None

    return date


def main():
    import yt_dlp  # noqa: E402
    args = parse_args()
    date = None
    audio_file = 'pre-audio.wav'
    video_id = args.video_id
    video_title = None

    # check if video is archived from stream-archiver
    if 'kyi-' not in args.video_id:
        URLS = [
            f'https://www.youtube.com/watch?v={args.video_id}'] if 'odysee' not in args.video_id else [f'{args.video_id}']

        ydl_opts = {
            'format': 'wav/bestaudio/best',
            'outtmpl': 'pre-audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(URLS[0], download=True)
            video_title = info_dict.get('title', None)

        video_id = args.video_id.split(
            '/')[-1] if 'odysee' in args.video_id else args.video_id
    else:
        # find .m4a file in this directory
        for file in os.listdir('.'):
            if file.endswith('.mp4'):
                audio_file = file
                date = int(file.split('-')[1].split('.')[0])
                video_id = args.video_id
                break

    # create whisperer
    whisperer = Whisperer(video_id=video_id, date=extract_date(
        video_title) if date is None else date, audio_file=audio_file)

    # transcribe
    try:
        segments = whisperer.transcribe()
        whisperer.write_to_csv()
    except Exception as e:
        whisperer.console.log(
            '❌ [bold red]Something went wrong w/whisperer')
        for file in os.listdir('.'):
            if file.endswith('.m4a') or file.endswith('.wav'):
                os.remove(file)
        try:
            os.remove('transcription.json')
        except:
            pass
        print(e)
        exit(1)

    # check if CONTAINERIZED env var is set
    if os.getenv('KYI_CONTAINERIZED') is None:
        # prompt user for y/Y/yes/Yes if they want to delete the audio file
        delete_audio = whisperer.console.input(
            '[bold cyan]Would you like to delete the corresponding files?[/] [bold white](y/n)[/]: ').lower()
        if delete_audio == 'y' or delete_audio == 'yes':
            # find any .m4a and .mp4 files in this directory
            for file in os.listdir('.'):
                if file.endswith('.m4a') or file.endswith('.mp4') or file.endswith('.wav'):
                    os.remove(file)
            try:
                os.remove('transcription.json')
            except:
                pass


if __name__ == '__main__':
    exit(main())
