import yt_dlp
import uuid
import os
import subprocess
import json

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    random_filename = str(uuid.uuid4())
    output_tmpl = os.path.join(DOWNLOAD_DIR, f"{random_filename}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_tmpl,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)
        final_wav_filename = os.path.join(DOWNLOAD_DIR, f"{random_filename}.wav")
    return final_wav_filename


def _get_audio_duration(wav_path: str) -> float:
    """Get audio duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", wav_path],
        check=True, capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to mono 16kHz WAV using ffmpeg."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    subprocess.run(
        ["ffmpeg", "-i", input_path, "-ac", "1", "-ar", "16000",
         output_path, "-y"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10):
    """Split WAV into chunks using ffmpeg."""
    chunk_sec = chunk_minutes * 60
    total_seconds = _get_audio_duration(wav_path)
    print(f"Audio Length: {total_seconds:.2f} seconds")

    chunks = []
    for i, start_sec in enumerate(range(0, int(total_seconds), chunk_sec)):
        chunk_path = f"{os.path.splitext(wav_path)[0]}_chunk_{i}.wav"

        subprocess.run(
            ["ffmpeg", "-i", wav_path, "-ss", str(start_sec),
             "-t", str(chunk_sec), "-ac", "1", "-ar", "16000",
             chunk_path, "-y"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
