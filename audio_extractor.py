# audio_extractor

from moviepy import VideoFileClip

def extract_audio_from_video(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        print(f"Audio extracted to {audio_path}")
    except Exception as e:
        print(f"Audio extraction failed: {e}")
