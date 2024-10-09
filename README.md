# GPT-Vision Webcam Frame Capture

This repository provides a Python script that lets you capture frames with your webcam and analyze them using OpenAI's GPT-4 Vision model. Press the spacebar to capture frames, and GPT-4 Vision will return quick, concise analysis, helpful for tasks like identifying materials for recycling.

## Features

- **Live Webcam Feed**: View your webcam feed live.
- **Frame Capture on Spacebar**: Capture frames when you press the spacebar.
- **AI-Powered Analysis**: GPT-4 Vision analyzes the captured frame and returns material identification and disposal guidance.
- **Simple Key Commands**: Use the spacebar to capture frames and **'q'** to quit.

---

## Prerequisites

Before you start, you’ll need:

- **Python 3.7+** installed on your system.
- **OpenCV** for capturing video frames.
- **OpenAI Python client** for connecting to GPT-4 Vision.
- An **OpenAI API key** with access to GPT-4 Vision.

---

## Setup Instructions

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/) and install it.
2. **IMPORTANT**: Check the box to **Add Python to PATH** during installation.

### Step 2: Install Required Libraries

Open Command Prompt and install the libraries using:
```bash
pip install opencv-python openai
```

### Step 3: Get OpenAI API Key

1. Sign up or log in to OpenAI at [platform.openai.com](https://platform.openai.com/).
2. Get your API key from the API settings page.
3. In the code, replace `"YOUR_API_KEY"` with your actual API key.

### Step 4: Prepare the Script

1. Copy the code below and paste it into a text editor (e.g., Notepad).
2. Save the file with the name `gpt_vision_webcam.py`.
3. Make sure the API key is correctly set in the code.

Or download the `gpt_vision_webcam.py` file directly from this repository, then edit it to add your API key.

### Python Code

```python
import cv2
import base64
import time
import threading
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

# Video capture setup
cap = cv2.VideoCapture(0)  # '0' is the default camera. Change if needed for external webcams.
frames_to_capture = 1  # Number of frames to capture each session
captured_frames = []

# Display live camera feed
def display_camera():
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Live Camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Capture frame on spacebar press
                capture_and_analyze_frames()
            elif key == ord('q'):  # Quit on 'q' press
                break
    cap.release()
    cv2.destroyAllWindows()

# Capture and analyze frames
def capture_and_analyze_frames():
    global captured_frames
    captured_frames = []
    print("Capturing and analyzing frames...")

    for _ in range(frames_to_capture):
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (500, 500))  # Resize for processing
        _, buffer = cv2.imencode(".jpg", resized_frame)
        encoded_frame = base64.b64encode(buffer).decode("utf-8")
        captured_frames.append(encoded_frame)
        time.sleep(0.1)

    # Send frames to GPT for analysis
    prompt_messages = [
        {"role": "user", "content": [
            "Identify materials in the image and provide recycling instructions.",
            *[{"image": x, "resize": 500} for x in captured_frames]
        ]}
    ]
    start_time = time.time()
    result = client.chat.completions.create(model="gpt-4-vision-preview", messages=prompt_messages, max_tokens=120)
    response_time = time.time() - start_time

    # Output results
    print(f"Response Time: {response_time:.2f} seconds")
    print(result.choices[0].message.content)

# Start camera thread
display_thread = threading.Thread(target=display_camera)
display_thread.start()
display_thread.join()
```

---

## How to Run on Windows

1. **Navigate to the script** in Command Prompt:
    ```bash
    cd path\to\your\script
    ```
2. Run the script with:
    ```bash
    python gpt_vision_webcam.py
    ```

### Interacting with the Script

- A window will display the live feed from your webcam.
- **Press spacebar** to capture a frame and analyze it.
- **Press 'q'** to quit the application.

---

## Troubleshooting

- **No module named 'cv2'**: Reinstall OpenCV with `pip install opencv-python-headless`.
- **API Key Issues**: Ensure the API key is set correctly in the script.

---

This setup should allow you to quickly capture and analyze frames using GPT-Vision on Windows. Adjust the `frames_to_capture` and `max_tokens` settings for customized responses. Enjoy experimenting!
