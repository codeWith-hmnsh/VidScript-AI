import os
import yt_dlp

def download_audio(url, output_path="downloads"):
    """
    Downloads best audio from a YouTube URL and returns (file_path, video_id, duration).
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info to get metadata and download
            info = ydl.extract_info(url, download=True)
            
            video_id = info.get('id')
            duration = info.get('duration')
            # The postprocessor changes the extension to .mp3
            file_path = os.path.join(output_path, f"{video_id}.mp3")
            
            if not os.path.exists(file_path):
                # Fallback in case postprocessor naming is different
                file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"

            return file_path, video_id, duration

    except yt_dlp.utils.DownloadError as e:
        raise ValueError(f"Download failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    try:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        path, vid, dur = download_audio(url)
        print(f"Path: {path}\nID: {vid}\nDuration: {dur}s")
    except Exception as e:
        print(f"Error: {e}")
