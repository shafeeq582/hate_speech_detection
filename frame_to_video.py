# frame_to_video

import cv2
import os

def create_video_from_frames(frames_folder, output_video_path, fps=30):
    frame_files = sorted(os.listdir(frames_folder))
    
    # Read the first frame to determine video dimensions
    first_frame = cv2.imread(os.path.join(frames_folder, frame_files[0]))
    if first_frame is None:
        print("Error: Could not read the first frame.")
        return
    
    height, width, _ = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for frame_file in frame_files:
        if frame_file.endswith(('.jpg', '.png')):
            frame_path = os.path.join(frames_folder, frame_file)
            frame = cv2.imread(frame_path)
            if frame is not None:
                video_writer.write(frame)
            else:
                print(f"Warning: Could not read frame {frame_file}")

    video_writer.release()
    print(f"Video saved to: {output_video_path}")
