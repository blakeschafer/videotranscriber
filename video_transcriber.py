import os
import whisper
import yt_dlp

VIDEO_DIR = "videos"
TRANSCRIPT_DIR = "transcripts"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(VIDEO_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'unknown')
        safe_title = clean_filename(title)
        # Get the actual filename yt-dlp wrote (it sanitizes special chars)
        downloaded = ydl.prepare_filename(info)
        audio_path = os.path.splitext(downloaded)[0] + ".mp3"
        return audio_path, safe_title


def clean_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()


def transcribe(audio_path, title):
    print(f"\nTranscribing: {title}")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    transcript_path = os.path.join(TRANSCRIPT_DIR, f"{title}.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Transcript saved to: {transcript_path}")
    return transcript_path


if __name__ == "__main__":
    url = input("\nEnter a YouTube video URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        exit(1)

    try:
        audio_path, title = download_youtube_video(url)
        transcribe(audio_path, title)
        print("\nDone!")
    except Exception as e:
        print(f"\nError: {e}")
        exit(1)
