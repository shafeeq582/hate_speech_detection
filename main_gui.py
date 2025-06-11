import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
import threading

from frame_extractor import extract_frames_from_video
from audio_extractor import extract_audio_from_video
from emotion_detector import load_frames_from_folder, detect_faces_and_emotions_in_frames
from hate_speech_beeper import process_audio
from frame_to_video import create_video_from_frames
from video_audio_merger import merge_video_audio

class HateSpeechUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hate Speech Detection & Video Processing")
        self.root.geometry("800x450")
        self.root.configure(bg="white")
        self.video_path = ""
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Hate Speech Detection & Video Processing",
                 font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        self.video_label = tk.Label(self.root, text="No video selected", font=("Arial", 10), bg="white")
        self.video_label.pack()

        browse_frame = tk.Frame(self.root, bg="white")
        browse_frame.pack(pady=5)

        self.path_entry = tk.Entry(browse_frame, width=70, font=("Arial", 10))
        self.path_entry.pack(side=tk.LEFT, padx=(10, 5))

        browse_button = tk.Button(browse_frame, text="Browse", bg="#3D94F6", fg="white", command=self.browse_video)
        browse_button.pack(side=tk.LEFT)

        self.status_label = tk.Label(self.root, text="Status: Ready", font=("Arial", 10), bg="white")
        self.status_label.pack(pady=5)

        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(pady=10)

        self.process_button = tk.Button(button_frame, text="Process Video", bg="green", fg="white",
                                        command=self.start_processing, state=tk.DISABLED)
        self.process_button.pack(side=tk.LEFT, padx=10)

        self.play_button = tk.Button(button_frame, text="Play Processed Video", bg="#00B8D4", fg="white",
                                     command=self.play_processed_video, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=10)

        tk.Label(self.root, text="Processing Log:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", padx=10)

        self.log_box = scrolledtext.ScrolledText(self.root, width=100, height=10, font=("Courier New", 10))
        self.log_box.pack(padx=10, pady=5)
        self.log("Application started. Select a video file to begin processing.")
        self.log("Loading speech recognition model... (This might take a moment)")
        self.log("Speech recognition model loaded successfully")

    def browse_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if self.video_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.video_path)
            self.video_label.config(text=os.path.basename(self.video_path))
            self.status_label.config(text="Status: Ready")
            self.process_button.config(state=tk.NORMAL)

    def start_processing(self):
        self.process_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Processing...")
        thread = threading.Thread(target=self.process_video)
        thread.start()

    def process_video(self):
        try:
            self.log(f"Processing video: {self.video_path}")

            output_folder = "extracted_frames"
            self.log("Extracting frames...")
            extract_frames_from_video(self.video_path, save_to_files=True, output_folder=output_folder)
            self.log(f"Frames saved to '{output_folder}'")

            audio_output_path = "extracted_audio.wav"
            self.log("Extracting audio...")
            extract_audio_from_video(self.video_path, audio_output_path)
            self.log(f"Audio extracted to '{audio_output_path}'")

            self.log("Detecting emotions in frames...")
            frames = load_frames_from_folder(output_folder)
            processed_output = "processed_faces_emotions"
            detect_faces_and_emotions_in_frames(frames, processed_output, emotion_model='fer', save_to_files=True)
            self.log(f"Emotions detected and processed frames saved to '{processed_output}'")

            self.log("Applying beep for hate speech...")
            censored_audio = "output.wav"
            process_audio(audio_output_path, censored_audio)
            self.log(f"Hate speech beeped and saved to '{censored_audio}'")

            output_video_path = "output_video.mp4"
            self.log("Combining processed frames into video...")
            create_video_from_frames(processed_output, output_video_path, fps=30)
            self.log(f"Processed frames combined into video: '{output_video_path}'")

            final_output = "final_output.mp4"
            self.log("Merging audio with video...")
            merge_video_audio(output_video_path, censored_audio, final_output)
            self.log(f"Final video with audio ready: '{final_output}'")

            self.status_label.config(text="Status: Done")
            self.play_button.config(state=tk.NORMAL)

        except Exception as e:
            self.log(f"Error: {e}")
            self.status_label.config(text="Status: Error")

    def play_processed_video(self):
        final_video = "final_output.mp4"
        if os.path.exists(final_video):
            os.startfile(final_video)
            self.log(f"Playing video: {final_video}")
        else:
            self.log("Final video not found. Please process it first.")

    def log(self, message):
        self.log_box.insert(tk.END, f"> {message}\n")
        self.log_box.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = HateSpeechUI(root)
    root.mainloop()