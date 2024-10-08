import cv2
import base64
import time
import threading
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

# Video capture setup
cap = cv2.VideoCapture(0) #0 is your camera source, and 0 is the default, if you encounter issues, usually with USB webcams, try other numbers.
frames_to_capture = 1  # Define the number of frames to capture per session (SUGGESTED UP TO 10)
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
    prompt_messages = [{"role": "user", "content": ["YOUR_PROMPT ON THE SAME LINE", *[{"image": x, "resize": 500} for x in captured_frames]]}]
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