# Video Transcriber

A Python tool that downloads a YouTube video and transcribes it to text using OpenAI's Whisper model.

## Prerequisites

- Python 3
- [ffmpeg](https://ffmpeg.org/) installed on your system (`brew install ffmpeg` on macOS)

## Usage

```bash
bash run.sh
```

The script will:

1. Set up a Python virtual environment and install dependencies
2. Prompt you to paste a YouTube video URL
3. Download the audio from the video
4. Transcribe it using Whisper
5. Save the transcript as a `.txt` file in the `transcripts/` folder

## Project Structure

```
run.sh                 # Entry point — sets up env and runs the script
video_transcriber.py   # Downloads and transcribes YouTube videos
requirements.txt       # Python dependencies
videos/                # Downloaded audio files
transcripts/           # Output transcript text files
```
