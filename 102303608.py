import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment


def create_folders():
    folders = ["audios", "cuts", "output"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


def download_audios(singer, n):
    query = f"ytsearch{n}:{singer} song"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audios/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])


def cut_audios(duration_sec):
    files = os.listdir("audios")
    for file in files:
        if file.endswith(".mp3"):
            path = os.path.join("audios", file)
            audio = AudioSegment.from_mp3(path)
            cut_audio = audio[:duration_sec * 1000]
            cut_audio.export(os.path.join("cuts", file), format="mp3")


def merge_audios(output_file):
    final_audio = AudioSegment.empty()

    files = os.listdir("cuts")
    for file in files:
        if file.endswith(".mp3"):
            audio = AudioSegment.from_mp3(os.path.join("cuts", file))
            final_audio += audio

    final_audio.export(os.path.join("output", output_file), format="mp3")


def cleanup():
    shutil.rmtree("audios", ignore_errors=True)
    shutil.rmtree("cuts", ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <RollNumber>.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit()

    singer_name = sys.argv[1]
    output_file = sys.argv[4]

    try:
        n = int(sys.argv[2])
        duration = int(sys.argv[3])
    except:
        print("Error: NumberOfVideos and AudioDuration must be integers")
        sys.exit()

    if n <= 10:
        print("Error: NumberOfVideos must be greater than 10")
        sys.exit()

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds")
        sys.exit()

    if not output_file.endswith(".mp3"):
        print("Error: OutputFileName must end with .mp3")
        sys.exit()

    try:
        create_folders()
        print(f"Downloading {n} videos for {singer_name}...")
        download_audios(singer_name, n)

        print(f"Cutting first {duration} seconds from each audio...")
        cut_audios(duration)

        print("Merging audios...")
        merge_audios(output_file)

        cleanup()

        print(f"SUCCESS: Mashup created in output/{output_file}")

    except Exception as e:
        print("ERROR:", str(e))