import json
import os
from datetime import datetime, timedelta

def format_duration(seconds):
    """Converts seconds to HH:MM:SS format."""
    return str(timedelta(seconds=int(seconds)))

def get_unique_filename(base, extension):
    """Checks if a file exists and returns a new name with a counter if it does."""
    filename = f"{base}.{extension}"
    if not os.path.exists(filename):
        return filename
    
    counter = 1
    while os.path.exists(f"{base}_{counter:02d}.{extension}"):
        counter += 1
    return f"{base}_{counter:02d}.{extension}"

def save_final_outputs(metadata, segments, output_base="transcript"):
    """
    Saves the final transcript in the EXACT JSON format required by the contract
    and a clean TXT version. Automatically prevents overwriting.
    """
    plain_text = "\n".join([f"[{format_duration(s['start'])}] {s['text']}" for s in segments])
    
    # Calculate simple quality score (0-100)
    duration = metadata.get("duration", 1)
    seg_count = len(segments)
    base_score = 100
    issues = []
    
    if seg_count == 0:
        base_score = 0
        issues.append("No speech detected")
    elif seg_count < (duration / 60):
        base_score -= 30
        issues.append("Very low speech density detected")
        
    quality_score = max(0, base_score)
    needs_review = quality_score < 70

    # The "Contract" JSON Shape
    final_data = {
        "video_url": metadata.get("url"),
        "video_id": metadata.get("video_id"),
        "audio_file": metadata.get("audio_file"),
        "model_used": metadata.get("model"),
        "language": metadata.get("language"),
        "duration": format_duration(duration),
        "number_of_chunks": metadata.get("number_of_chunks"),
        "status": "success",
        "quality": {
            "score": quality_score,
            "issues": issues,
            "needs_manual_review": needs_review
        },
        "transcript": [
            {
                "start": format_duration(s["start"]),
                "end": format_duration(s["end"]),
                "text": s["text"]
            } for s in segments
        ],
        "plain_text": plain_text
    }

    # Generate Unique Filenames
    json_path = get_unique_filename(output_base, "json")
    txt_path = get_unique_filename(output_base, "txt")

    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)
    
    # Save TXT
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plain_text)
            
    return final_data, json_path, txt_path

def print_summary(report_data):
    """Prints a clean summary to the console."""
    q = report_data["quality"]
    print("\n" + "="*35)
    print("      FINAL PROJECT REPORT")
    print("="*35)
    print(f"Video ID:      {report_data['video_id']}")
    print(f"Language:      {report_data['language'].upper()}")
    print(f"Duration:      {report_data['duration']}")
    print(f"Quality Score: {q['score']}/100")
    print(f"Review Needed: {'REQUIRED' if q['needs_manual_review'] else 'No'}")
    if q["issues"]:
        print(f"Issues:        {', '.join(q['issues'])}")
    print("="*35 + "\n")

if __name__ == "__main__":
    print("Report module ready.")
