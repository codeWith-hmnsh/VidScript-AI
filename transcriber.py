from faster_whisper import WhisperModel
from tqdm import tqdm

def transcribe_audio(file_path, model_name="base", device="cpu", language=None):
    """
    Transcribes an audio file using Faster-Whisper and returns detailed metadata.
    """
    model = WhisperModel(model_name, device=device, compute_type="int8")
    
    # Use manual language if provided, otherwise let it auto-detect
    print(f"  [AI] Transcribing {info_duration if 'info_duration' in locals() else ''} audio...")
    segments, info = model.transcribe(file_path, beam_size=5, language=language)
    
    result_segments = []
    
    # Add a progress bar based on the duration of the audio
    print(f"  [AI] Transcribing {info.duration:.2f}s of audio...")
    with tqdm(total=info.duration, unit="s", desc="  Processing", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}s") as pbar:
        for segment in segments:
            result_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
            # Update the progress bar to the end of the current segment
            pbar.update(segment.end - pbar.n)
        
        # Ensure the progress bar reaches 100%
        pbar.update(info.duration - pbar.n)
        
    return {
        "segments": result_segments,
        "language": info.language,
        "model_name": model_name
    }

def transcribe_chunks(chunk_paths, model_name="base", language=None):
    """
    Transcribes a list of audio chunks and returns a list of results.
    """
    results = []
    for path in tqdm(chunk_paths, desc="Transcribing chunks"):
        result = transcribe_audio(path, model_name, language=language)
        results.append(result)
    return results

if __name__ == "__main__":
    print("Transcriber module ready.")
