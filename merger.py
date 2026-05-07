def merge_results(transcription_results, chunk_length_s=600, overlap_s=5):
    """
    Merges multiple chunk transcription results into a single list of segments.
    Adjusts timestamps and performs basic overlap removal.
    """
    merged_segments = []
    
    for i, result in enumerate(transcription_results):
        # Calculate offset for this chunk (in seconds)
        offset = i * (chunk_length_s - overlap_s)
        
        for segment in result["segments"]:
            adjusted_segment = {
                "start": segment["start"] + offset,
                "end": segment["end"] + offset,
                "text": segment["text"]
            }
            
            # Simple overlap handling: 
            # If this segment starts before the last merged segment ends, skip it if they are identical or too close.
            if merged_segments:
                last_segment = merged_segments[-1]
                if adjusted_segment["start"] < last_segment["end"]:
                    # If the text is very similar or it's a direct duplicate, skip
                    if adjusted_segment["text"] == last_segment["text"]:
                        continue
                    # Or if it starts significantly before the last one ends, it might be a partial duplicate
                    if adjusted_segment["start"] < last_segment["end"] - 1: # more than 1s overlap
                         continue
            
            merged_segments.append(adjusted_segment)
            
    return merged_segments

def format_as_text(segments):
    """
    Converts a list of segments into a readable transcript string.
    """
    lines = []
    for seg in segments:
        timestamp = f"[{int(seg['start']//60):02d}:{int(seg['start']%60):02d}]"
        lines.append(f"{timestamp} {seg['text']}")
    return "\n".join(lines)

def save_transcript(text, output_file="transcript.txt"):
    """
    Saves the final transcript to a text file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    return output_file
