#extract frames

import cv2
import os

# Function to extract frames from video and store them as files or in memory
def extract_frames_from_video(video_path, save_to_files=True, output_folder="extracted_frames"):
    video = cv2.VideoCapture(video_path)  # Open the video file
    frames = []  # List to store frames in memory

    # If you want to store frames as files
    if save_to_files and output_folder:
        os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

    frame_number = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break  # End of video

        # Store the frame in memory 
        if not save_to_files:
            frames.append(frame)
        else:
            # Save the frame as an image file in the specified folder
            frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_number += 1
    
    video.release()  # Release the video capture object



    print(f"Frames saved to {output_folder}")
    return None  # Return None as frames are saved as files


