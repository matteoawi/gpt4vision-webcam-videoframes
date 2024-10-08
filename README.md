# gpt4vision-webcam-videoframes

# Running GPT-Vision with Webcam for Frame Capture

This guide demonstrates how to set up and use GPT-Vision locally. Using a webcam, you can capture frames by pressing the spacebar and send them to the model for analysis. The setup uses OpenAI’s GPT-4 Vision preview model for visual understanding and quick responses.

## Prerequisites

- Python 3.7 or higher
- OpenCV for video capture and frame manipulation
- OpenAI Python client for API interaction
- An API key from OpenAI with access to GPT-4 Vision preview

## Installation

Install the required libraries:
```bash
pip install opencv-python-headless openai
```

## Usage

The script allows you to:
1. Display a live feed from your webcam.
2. Capture a frame when you press the spacebar.
3. Send the frame to GPT-Vision for analysis, with a focus on efficient garbage sorting by material identification.

In this script we can process up to **10 frame per request** and returns concise responses with a maximum token limit of **120 tokens**.
Feel free to play with this 2 numbers for achieving your goals.

## Code Implementation

Here's the Python code to set up the webcam and integrate it with GPT-Vision:

```python
import cv2
import base64
import time
import threading
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

# Video capture setup
cap = cv2.VideoCapture(0) #0 is your camera source, and 0 is the default, if you encounter issues, usually with USB webcams, try other numbers.
frames_to_capture = 1  # Define the number of frames to capture per session
captured_frames = []

# Threaded function to display live camera feed
def display_camera():
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Live Camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Start capturing on spacebar press
                capture_and_analyze_frames()
            elif key == ord('q'):  # Exit on 'q' key
                break
    cap.release()
    cv2.destroyAllWindows()

# Function to capture and analyze frames
def capture_and_analyze_frames():
    global captured_frames
    captured_frames = []
    print("Capturing and analyzing frames...")

    # Capture, resize, and encode frames
    for _ in range(frames_to_capture):
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (500, 500))  # Resize to 500x500
        _, buffer = cv2.imencode(".jpg", resized_frame)
        encoded_frame = base64.b64encode(buffer).decode("utf-8")
        captured_frames.append(encoded_frame)
        time.sleep(0.1)

    # Prepare frames for GPT and measure processing time
    prompt_messages = [{"role": "user", "content": ["Assisti nella differenziazione dei rifiuti analizzando i materiali nell'immagine: identifica il materiale o i materiali e fornisci istruzioni di smaltimento. Risposta secca, no yapping", *[{"image": x, "resize": 500} for x in captured_frames]]}]
    start_time = time.time()
    result = client.chat.completions.create(model="gpt-4-vision-preview", messages=prompt_messages, max_tokens=120)
    response_time = time.time() - start_time

    # Output results
    print(f"Response Time: {response_time:.2f} seconds")
    print(result.choices[0].message.content)

# Start camera display thread
display_thread = threading.Thread(target=display_camera)
display_thread.start()
display_thread.join()
```

## Explanation

### Key Functions

- **display_camera()**: Continuously displays the webcam feed and listens for key presses (`space` for capturing, `q` for quitting).
- **capture_and_analyze_frames()**: Captures, resizes, and encodes frames, then sends them to GPT-Vision for analysis. The response includes material identification and disposal instructions.

### Settings

- **frames_to_capture**: Number of frames to capture per session.
- **max_tokens**: Sets the maximum response length from GPT (120 tokens for concise feedback).
- **resize dimensions**: Frames are resized to 500x500 for optimal processing.

## Notes

- To quit the application, press **'q'**.
- Make sure to replace `"YOUR_API_KEY"` with your actual OpenAI API key.

Here are step-by-step instructions to run this GPT-Vision project on Windows.

--------------------------------------------------------------

### Running GPT-Vision Webcam Capture on Windows

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/) and install it on your system. 
2. Ensure the option **"Add Python to PATH"** is selected during installation.

#### Step 2: Install Required Libraries

Open Command Prompt and install the necessary libraries:
```bash
pip install opencv-python-headless openai
```

#### Step 3: Get OpenAI API Key

1. Go to [OpenAI's API site](https://platform.openai.com/) and sign up or log in.
2. Generate an API key from the API settings page.
3. Replace `"YOUR_API_KEY"` in the code with your actual API key.

#### Step 4: Prepare the Python Script

1. Copy the code provided and paste it into a text editor like **Notepad**.
2. Save the file with a `.py` extension (e.g., `gpt_vision_webcam.py`).
3. Make sure the script has your API key configured.

#### Step 5: Run the Script

1. Open Command Prompt and navigate to the folder containing the saved `.py` file:
    ```bash
    cd path\to\your\script
    ```
2. Run the script by typing:
    ```bash
    python gpt_vision_webcam.py
    ```

#### Step 6: Interact with the Script

- A window should open displaying the live feed from your webcam.
- Press **spacebar** to capture a frame for analysis.
- Press **'q'** to close the webcam and end the script.

#### Troubleshooting

- **Error: "No module named 'cv2'"** – Make sure OpenCV was installed correctly with `pip install opencv-python-headless`.
- **API Authentication Error** – Double-check that your API key is correct and placed in the script where it says `"YOUR_API_KEY"`.

---

This setup should allow you to run the script on Windows and capture frames with the spacebar to analyze them using GPT-Vision.
