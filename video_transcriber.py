# requirements.txt
# ffmpeg-python
# pytube
# openai-whisper
# torch
# rich
# beautifulsoup4
# requests

import os
import shutil
import whisper
import requests
from pytube import YouTube
from bs4 import BeautifulSoup
from rich.progress import Progress

# Directory to save videos and transcripts
VIDEO_DIR = "videos"
TRANSCRIPT_DIR = "transcripts"

# Create directories if they don't exist
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

def fetch_archive_video_links(archive_url):
    response = requests.get(archive_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.mp4'):
            full_url = f"https://archive.org{href}"
            video_urls.append(full_url)
    return video_urls

def download_video(url):
    local_filename = url.split("/")[-1]
    local_path = os.path.join(VIDEO_DIR, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path, os.path.splitext(local_filename)[0]

def transcribe_video(video_path, title):
    print(f"🧠 Transcribing: {video_path}")
    try:
        model = whisper.load_model("base")
        result = model.transcribe(video_path)
        transcript_path = os.path.join(TRANSCRIPT_DIR, f"{title}.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"✅ Transcript saved to: {transcript_path}")
        return transcript_path
    except Exception as e:
        print(f"❌ Transcription failed for {video_path}: {e}")
        return None

def clean_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()

def process_video(url):
    print(f"\nProcessing: {url}")
    video_path, title = download_video(url)
    title = clean_filename(title)
    print(f"Downloaded: {title}")
    transcript_path = transcribe_video(video_path, title)
    if transcript_path:
        print(f"Transcript saved: {transcript_path}")
    else:
        print(f"No transcript saved for: {title}")

if __name__ == "__main__":
    archive_page_url = "https://archive.org/details/OldSneako"
    video_urls = fetch_archive_video_links(archive_page_url)

    with Progress() as progress:
        task = progress.add_task("Transcribing videos...", total=len(video_urls))
        for url in video_urls:
            try:
                process_video(url)
            except Exception as e:
                print(f"Error processing {url}: {e}")
            progress.update(task, advance=1)

    print("\nAll done!")
