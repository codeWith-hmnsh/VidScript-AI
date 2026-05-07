import argparse
import sys
import os
from downloader import download_audio
from audio_processor import process_audio
from transcriber import transcribe_audio, transcribe_chunks
from merger import merge_results
from report import save_final_outputs, print_summary

def main():
    parser = argparse.ArgumentParser(description="VidScript AI: Convert YouTube videos to transcripts.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--output", "-o", default="transcript", help="Output base filename (default: transcript)")
    parser.add_argument("--model", "-m", default="base", help="Whisper model: tiny, base, small, medium, large (default: base)")
    parser.add_argument("--language", "-l", default=None, help="Force language (e.g., hi, en, es)")
    
    args = parser.parse_args()
    
    print("\n--- VidScript AI CLI ---")
    print(f"Target URL: {args.url}\n")
    
    try:
        # 1. Download
        print("[Step 1/4] Downloading best audio...")
        audio_file, video_id, duration = download_audio(args.url)
        print(f"  ✓ Downloaded as {video_id}.mp3 ({duration}s)")
        
        # 2. Process
        print("[Step 2/4] Processing audio (16kHz WAV + chunking)...")
        audio_chunks = process_audio(audio_file)
        print(f"  ✓ Created {len(audio_chunks)} processing chunk(s)")
        
        # 3. Transcribe
        print(f"[Step 3/4] Transcribing using '{args.model}' model...")
        lang_code = args.language
        
        if len(audio_chunks) == 1:
            result = transcribe_audio(audio_chunks[0], model_name=args.model, language=lang_code)
            final_segments = result["segments"]
            detected_lang = result["language"]
        else:
            chunk_results = transcribe_chunks(audio_chunks, model_name=args.model, language=lang_code)
            final_segments = merge_results(chunk_results)
            detected_lang = chunk_results[0]["language"]
        print(f"  ✓ Transcription complete (Language: {detected_lang})")
            
        # 4. Final Save & Report
        print("[Step 4/4] Saving outputs and generating quality report...")
        report_data, json_file, txt_file = save_final_outputs({
            "url": args.url,
            "video_id": video_id,
            "audio_file": f"{video_id}.mp3",
            "model": args.model,
            "language": detected_lang,
            "duration": duration,
            "number_of_chunks": len(audio_chunks)
        }, final_segments, args.output)
        
        # Final Summary to Console
        print_summary(report_data)
        print(f"Files saved: {json_file}, {txt_file}")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
