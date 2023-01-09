import whisper
import sys
import csv
import argparse
import yt_dlp
import json

class Whisperer:
    def __init__(self, model: str = 'base', video_id: str = None, date: int = None):
        self.model = whisper.load_model(model)
        self.video_id = video_id
        self.segments = []
        self.date = date

    def transcribe(self):
        self.segments = self.__coalesce_segments()
        return self.segments

    def __coalesce_segments(self):
        result = self.model.transcribe('audio.m4a')
        segments = result['segments']
        coalesced_segments = []
        for segment in segments:
            if len(coalesced_segments) == 0:
                coalesced_segments.append(segment)
            else:
                last_segment = coalesced_segments[-1]
                if (int(segment['start']) - int(last_segment['end'])) < 30 and len(last_segment['text'].split()) < 40:
                    last_segment['end'] = segment['end']
                    last_segment['text'] += segment['text']
                else:
                    coalesced_segments.append(segment)

        # map a list of segments to convert the start and end times to ints
        coalesced_segments = list(map(lambda segment: {'start': int(
            segment['start']), 'text': segment['text']}, coalesced_segments))
        return coalesced_segments

    def write_to_csv(self):
        with open(f'./transcripts/{self.video_id}.csv', 'w') as f:
            # write header
            f.write('video_id,date,start,text\n')

            # write segments
            for segment in self.segments:
                f.write(
                    f'{self.video_id},{self.date},{segment["start"]},{segment["text"].strip()}\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id', help='The Video ID of the YouTube video being transcribed, e.g. "NyiJDDyUV54"',
                        type=str)
    parser.add_argument('--model', help='The Whisper model being used, e.g. "base" or "large". Depends on your hardware. See https://github.com/openai/whisper#available-models-and-languages to see which models your system can run. Default is "base".',
                        type=str, default='base.en', required=False)
    return parser.parse_args()

def extract_date(title: str):
    title = title.replace('(','').replace(')','')
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

    return date

def main():
    args = parse_args()

    if '.en' not in args.model and args.model != 'large':
        args.model = args.model + '.en'

    import yt_dlp

    URLS = [f'https://www.youtube.com/watch?v={args.video_id}']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'audio.m4a',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(URLS[0], download=False)
        video_title = info_dict.get('title', None)
        error_code = ydl.download(URLS)

    # create whisperer
    whisperer = Whisperer(model=args.model, video_id=args.video_id, date=extract_date(video_title))

    # transcribe
    segments = whisperer.transcribe()
    whisperer.write_to_csv()


if __name__ == '__main__':
    exit(main())
