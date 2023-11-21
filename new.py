import cv2
import pytesseract
import subprocess
import os

# Path to your Tesseract installation directory
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to your input video
input_video_path = 'temp.mp4'
# Path to your output video
output_video_path = 'output_video.mp4'
# Path to directory to save extracted frames
frames_directory = 'frames/'

# Create the frames directory if it doesn't exist
os.makedirs(frames_directory, exist_ok=True)

# Function to extract frames from the video
def extract_frames(video_path, output_directory):
    cap = cv2.VideoCapture(video_path)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_path = os.path.join(output_directory, f'frame_{str(count).zfill(4)}.png')
        cv2.imwrite(frame_path, frame)
        count += 1

    cap.release()

# Function to perform OCR using Tesseract on an image
def perform_ocr(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image '{image_path}' not found or cannot be read.")

        # Convert the image to RGB format (Tesseract expects RGB)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Perform OCR on the RGB image
        extracted_text = pytesseract.image_to_string(rgb_image)
        return extracted_text
    except Exception as e:
        print(f"Error occurred while performing OCR: {e}")
        return ''

# Function to replace text in the video frames
def replace_text_in_frames(frames_directory):
    detected_text = 'SUBSCRIBE'  # Replace with the text you want to detect
    new_text = 'ANSHUL'  # Replace with the text you want to insert

    for i in range(1000):  # Modify the range based on the number of frames
        frame_path = os.path.join(frames_directory, f'frame_{str(i).zfill(4)}.png')
        extracted_text = perform_ocr(frame_path)

        if detected_text in extracted_text:
            modified_text = extracted_text.replace(detected_text, new_text)
            cv2.imwrite(frame_path, cv2.putText(cv2.imread(frame_path), modified_text, (50, 100),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA))

# Execute functions
extract_frames(input_video_path, frames_directory)
replace_text_in_frames(frames_directory)

# Execute FFmpeg command to create a new video from modified frames
ffmpeg_cmd = f'ffmpeg -framerate 30 -i {frames_directory}frame_%04d.png -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k {output_video_path}'
subprocess.call(ffmpeg_cmd, shell=True)
