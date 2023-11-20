import os
import cv2
import time
import json

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

def setup_camera(camera_info):
    rtsp_url = camera_info.get("url", "")
    camera_title = camera_info.get("title", "")

    if not rtsp_url:
        print(f"Error: RTSP URL not found for {camera_title}. Check the setup.json file.")
        return None, None

    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"Error: Could not open the camera for {camera_title}.")
        return None, None

    return cap, camera_title

# Load camera setups from setup.json
with open('setup.json', 'r') as file:
    setup_data = json.load(file)

# Create folders for each camera inside the screenshots directory
image_folder = 'screenshots/'
os.makedirs(image_folder, exist_ok=True)

camera_caps = {}
for camera_name, camera_info in setup_data.items():
    cap, title = setup_camera(camera_info)
    if cap is not None and title is not None:
        camera_caps[camera_name] = {"cap": cap, "title": title}

interval_seconds = 5
last_capture_time = time.time()

jpeg_quality = 90  # Adjust this value to control the image quality (0-100)

# Set the window size to 800x600 for each camera
# Comment out the following lines to remove the windows
# for camera_name, camera_info in camera_caps.items():
#     title = camera_info["title"]
#     cv2.namedWindow(f'Live Stream - {title}', cv2.WINDOW_NORMAL)
#     cv2.resizeWindow(f'Live Stream - {title}', 800, 600)

while True:
    for camera_name, camera_info in camera_caps.items():
        cap = camera_info["cap"]
        title = camera_info["title"]

        ret, frame = cap.read()

        if not ret:
            print(f"Error: Could not read frame from {title}.")
            continue

        # Display the live stream for each camera with title
        # Comment out the following line to remove the display
        # cv2.imshow(f'Live Stream - {title}', frame)

        current_time = time.time()
        if current_time - last_capture_time >= interval_seconds:
            
            timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
            folder_write = os.path.join(image_folder, title, str(time.strftime('%Y-%m-%d')))
            
            if os.path.exists(folder_write):
                print(timestamp)
            else:
                print(f"Failed to create directory '{folder_write}'.")
                os.makedirs(folder_write)
            
            image_path = os.path.join(folder_write, f'image_{timestamp}.jpg')  # Use .jpg extension
            cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            last_capture_time = current_time
            print(f'Image captured and saved for {title}: {image_path}')

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the cameras and close the OpenCV windows
for camera_info in camera_caps.values():
    cap = camera_info["cap"]
    cap.release()

# Comment out the following line to remove the window destruction
# cv2.destroyAllWindows()
