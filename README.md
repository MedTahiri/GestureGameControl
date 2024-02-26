# Hand Gesture Game Controller

## Overview
The Hand Gesture Game Controller project revolutionizes gaming by enabling players to interact with games using hand gestures instead of traditional keyboards. By leveraging computer vision techniques and advanced hand tracking algorithms, this system interprets hand movements and translates them into game controls.

## Features
- **Control by Hand:** Utilizes the `mediapipe` library for real-time hand tracking, empowering users to control the game by moving their hands in front of the camera.
- **Control by Finger Gestures:** Incorporates the `cvzone` library to recognize intricate finger gestures, offering a wide range of game control options beyond basic hand movements.
- **Multi-camera Support:** Provides flexibility with support for multiple camera sources, allowing users to choose the most suitable setup for their gaming environment.

## Requirements
- Python 3.8.10
- OpenCV (`cv2`)
- Mediapipe (`mediapipe`)
- Pynput (`pynput`)
- Tkinter (`tkinter`)
- Pillow (`PIL`)
- Cvzone (`cvzone`)

## Installation
1. Ensure you have Python 3.8.10 installed on your system.
2. Install the required Python packages using the following command:
   ```bash
   pip install opencv-python mediapipe pynput Pillow cvzone
   ```

## Usage
1. Launch the application.
2. Use the "Control by Hand" section to control the game by moving your hand within the camera's field of view.
3. Utilize the "Control by Finger" section to trigger specific game actions by performing predefined finger gestures.
4. Press the "Start" button to initiate camera input and activate control functionalities.
5. Press the "Stop" button to terminate camera input and deactivate control functionalities.

## Contributions
Contributions are welcome! If you have any ideas for improvements or additional features, feel free to open an issue or submit a pull request.
