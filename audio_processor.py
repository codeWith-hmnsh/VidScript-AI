import os
from pydub import AudioSegment

def process_audio(input_file, output_dir="processed"):
    """
    Converts audio to 16kHz WAV and splits into overlapping chunks if > 10 mins.
    Returns a list of file paths.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Load and convert to 16kHz mono WAV
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    duration_mins = len(audio) / (1000 * 60)
    
    # 2. Check if splitting is needed (> 10 mins)
    if duration_mins <= 10:
        output_file = os.path.join(output_dir, "full_audio.wav")
        audio.export(output_file, format="wav")
        return [output_file]
    
    # 3. Split into 10-minute chunks with 5-second overlap
    chunk_length_ms = 10 * 60 * 1000  # 10 minutes
    overlap_ms = 5 * 1000            # 5 seconds
    
    chunks = []
    start = 0
    while start < len(audio):
        end = start + chunk_length_ms
        chunk = audio[start:end]
        
        chunk_name = os.path.join(output_dir, f"chunk_{len(chunks)}.wav")
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)
        
        # Increment start point by chunk length MINUS overlap
        start += (chunk_length_ms - overlap_ms)
        
        # Stop if we are near the end
        if start >= len(audio) - overlap_ms:
            break
            
    return chunks

if __name__ == "__main__":
    print("Audio processor module ready.")
