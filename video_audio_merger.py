# video_audio_merger

import os
import subprocess

def merge_video_audio(video_path, audio_path, output_path="final_output.mp4"):
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # Overwrite without prompt
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        output_path
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Final video with audio saved as: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during merge: {e}")
