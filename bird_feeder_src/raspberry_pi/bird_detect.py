import cv2
import time
import os
import json
import base64
import re
import subprocess
from picamera import PiCamera
from picamera.array import PiRGBArray
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR GEMINI API KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Create necessary directories
IMAGE_DIR = "static/images"
VIDEO_DIR = "static/videos"
DATA_FILE = "bird_data.json"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# Initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))
time.sleep(2)  # Allow camera to warm up

def load_bird_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"birds": []}

def save_bird_data(bird_info):
    data = load_bird_data()
    data["birds"].append(bird_info)
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def capture_image():
    timestamp = int(time.time())
    image_path = f"{IMAGE_DIR}/{timestamp}.jpg"
    raw_capture.truncate(0)
    camera.capture(raw_capture, format="bgr")
    image = raw_capture.array
    cv2.imwrite(image_path, image)
    return image_path, timestamp

def capture_video(timestamp):
    h264_path = f"{VIDEO_DIR}/{timestamp}.h264"
    mp4_path = f"{VIDEO_DIR}/{timestamp}.mp4"
    camera.start_recording(h264_path)
    camera.wait_recording(10)
    camera.stop_recording()

    # Convert to MP4
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "24", "-i", h264_path, "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "23", mp4_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(h264_path)  # Remove original .h264 file
    return mp4_path

def detect_bird(image_path):
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
        image_blob = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_data).decode("utf-8")
        }

    response = model.generate_content([
        {"role": "user", "parts": [{"inline_data": image_blob}]},
        {"role": "user", "parts": [{"text": "Does this image contain a bird? Respond with 'yes' or 'no'."}]}
    ])

    response_text = response.text.strip().lower() if hasattr(response, "text") else ""
    return "yes" in response_text

def identify_bird(image_path):
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
        image_blob = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_data).decode("utf-8")
        }

    response_info = model.generate_content([
        {"role": "user", "parts": [{"inline_data": image_blob}]},
        {"role": "user", "parts": [{"text": "Identify this bird and return details in JSON format: {\"name\": \"<bird name>\", \"scientific_name\": \"<scientific name>\", \"habitat\": \"<habitat>\", \"diet\": \"<diet>\", \"info\": \"<fun fact>\"}. Only return JSON."}]}
    ])

    raw_response = response_info.text.strip() if hasattr(response_info, "text") else ""

    try:
        cleaned_response = re.sub(r"^```json|```$", "", raw_response).strip()
        bird_info = json.loads(cleaned_response)
    except json.JSONDecodeError:
        bird_info = {
            "name": "Unknown",
            "scientific_name": "Unknown",
            "habitat": "Unknown",
            "diet": "Unknown",
            "info": "No details available."
        }

    return bird_info

# Main loop
MOTION_INTERVAL = 20
while True:
    image_path, timestamp = capture_image()
    print(f"Image saved: {image_path}")

    if detect_bird(image_path):
        print("Bird detected!")

        video_path = capture_video(timestamp)
        print(f"Video saved: {video_path}")

        bird_info = identify_bird(image_path)
        bird_info["image_path"] = image_path
        bird_info["video_path"] = video_path
        bird_info["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        save_bird_data(bird_info)

    else:
        print("No bird detected. Deleting image.")
        os.remove(image_path)

    time.sleep(MOTION_INTERVAL)

