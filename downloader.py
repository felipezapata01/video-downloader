import sys
import os
import argparse
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()

VIDEO_STORE_PATH = os.getenv('VIDEO_STORE_PATH')
AUDIO_STORE_PATH = os.getenv('AUDIO_STORE_PATH')

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--audio", help="Download audio only", action="store_true")
parser.add_argument("source", help="Youtube URL of the video to download")
parser.add_argument("file_name", help="Final filename in local system")

def progress_func(stream, bytes, bytes_remaining):
    total = stream.filesize
    downloaded = total - bytes_remaining
    completed = int(downloaded / total * 100)
    end = '\r' if completed < 100 else '\n'
    print(f"Downloading... [{'#' * completed}{'.' * (100 - completed)}] {completed}%", end=end)

def download(audio, source, file_name):
    try:
        yt = YouTube(source, on_progress_callback=progress_func)
    except:
        print('Connection Error')    
        
    try:
        if audio:
            media = yt.streams.get_audio_only()
            media.download(AUDIO_STORE_PATH, f'{file_name}.mp3')
        else:
            media = yt.streams.filter(file_extension='mp4').get_highest_resolution()
            media.download(VIDEO_STORE_PATH, f'{file_name}.mp4') 
    except Exception as e:
        print("There was an error during the download!", e) 
    else:
        print('Download completed successfully!')
    


def main() -> None:
    args = parser.parse_args()
    download(args.audio, args.source, args.file_name)

if __name__ == '__main__':
    main()


