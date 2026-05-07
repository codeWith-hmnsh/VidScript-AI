# VidScript AI: YouTube to Best Possible Transcript

VidScript AI is a modular Python CLI tool designed to generate high-quality, timestamped transcripts from YouTube videos using local AI models. Unlike standard auto-captions, this tool processes the actual audio directly to ensure maximum accuracy.

## Key Features
- **Local AI Transcription**: Powered by `faster-whisper` for fast, private, and accurate speech-to-text.
- **Intelligent Audio Pipeline**: Automatically converts audio to 16kHz WAV and handles long-form content by splitting it into overlapping chunks.
- **Multilingual Support**: Automatically detects and transcribes over 99 languages (English, Hindi, Spanish, etc.).
- **Standardized Output**: Generates both a clean readable `.txt` file and a structured `.json` file containing full metadata and quality metrics.

## Installation

### 1. Prerequisites
- **Python 3.8 - 3.13**
- **FFmpeg**: Required for audio processing.
  - *Windows*: `winget install ffmpeg`
  - *Mac*: `brew install ffmpeg`

### 2. Setup
Clone this repository and install the dependencies:
```bash
pip install -r requirements.txt
```

*Note: If you are on Python 3.13, ensure `audioop-lts` is installed (included in requirements.txt).*

## Usage

Run the tool by providing a YouTube URL:
```bash
python main.py https://www.youtube.com/watch?v=EXAMPLE_ID
```

### Options
- `-o, --output`: Specify the base name for output files (default: `transcript`).
- `-m, --model`: Specify the Whisper model size (`tiny`, `base`, `small`, `medium`, `large`). Larger models are more accurate but slower.
  ```bash
  python main.py https://www.youtube.com/watch?v=EXAMPLE_ID -m small
  ```

## Project Structure
- `main.py`: Entry point and workflow orchestrator.
- `downloader.py`: YouTube audio extraction using `yt-dlp`.
- `audio_processor.py`: Audio conversion and chunking logic.
- `transcriber.py`: AI transcription using `faster-whisper`.
- `merger.py`: Chunk merging and timestamp alignment.
- `report.py`: Final file generation and quality scoring.

## JSON Contract
The system generates a `transcript.json` matching the following schema:
```json
{
  "video_url": "...",
  "video_id": "...",
  "audio_file": "...",
  "model_used": "...",
  "language": "...",
  "duration": "HH:MM:SS",
  "number_of_chunks": 1,
  "status": "success",
  "quality": {
    "score": 100,
    "issues": [],
    "needs_manual_review": false
  },
  "transcript": [
    { "start": "00:00:00", "end": "00:00:05", "text": "..." }
  ],
  "plain_text": "..."
}
```
