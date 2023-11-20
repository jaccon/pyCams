import os
import cv2
import glob
from datetime import datetime

def create_timelapse(input_folder, output_folder, fps=30):
    # Get a list of image files in the input directory
    image_files = sorted(glob.glob(os.path.join(input_folder, '*.jpg')))

    if not image_files:
        print("No image files found in the specified directory.")
        return

    # Create VideoWriter object
    frame = cv2.imread(image_files[0])
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v codec for MP4 format

    # Add date and time stamp to the output file name
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_video = os.path.join(output_folder, f'timelapse_output_{current_time}.mp4')

    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Process each image and write it to the video
    for image_file in image_files:
        img = cv2.imread(image_file)
        video.write(img)

    # Release VideoWriter object
    video.release()

if __name__ == "__main__":
    input_directory = 'screenshots/Garagem Interna/2023-11-13'  # Replace with the path to your image directory
    output_directory = 'videos/'  # Replace with the path to your output directory

    create_timelapse(input_directory, output_directory)
    print(f"Timelapse video created successfully in '{output_directory}'.")
