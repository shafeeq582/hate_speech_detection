# emotion_detector

import cv2
import os
from fer import FER

# Function to load frames from the folder
def load_frames_from_folder(folder_path):
    frames = []
    frame_files = sorted(os.listdir(folder_path))  # Sort to maintain order
    for frame_file in frame_files:
        if frame_file.endswith(('.jpg', '.png')):
            frame_path = os.path.join(folder_path, frame_file)
            frame = cv2.imread(frame_path)
            frames.append((frame_file, frame))  # Keep filename if needed
    return frames

# Detect emotions and annotate frames
def detect_faces_and_emotions_in_frames(frames, output_folder, emotion_model='fer', save_to_files=True):
    if emotion_model == 'fer':
        emotion_detector = FER()
    
    os.makedirs(output_folder, exist_ok=True)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for frame_number, (filename, frame) in enumerate(frames):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        emotions = emotion_detector.top_emotion(frame)
        emotion = emotions[0] if emotions else 'None'

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        if save_to_files:
            output_path = os.path.join(output_folder, f"processed_{filename}")
            cv2.imwrite(output_path, frame)

    print(f"Processed frames saved to '{output_folder}'")
