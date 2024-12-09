import cv2
import mediapipe as mp
from math import atan2
from pynput.keyboard import Controller, Key
import time

def get_finger_direction(angle):
    if angle < -45 and angle > -135:
        return "Down"
    elif angle >= 45 and angle < 135:
        return "Up"
    elif angle >= 135 or angle < -135:
        return "Left"
    else:
        return "Right"

open = True

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Initialize video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get landmark coordinates
            landmark_coords = [(int(l.x * frame.shape[1]), int(l.y * frame.shape[0])) for l in hand_landmarks.landmark]

            # Extract fingertip coordinates (thumb, index, middle, ring, pinky)
            # Index 4, 8, 12, 16, and 20 are the fingertips
            thumb_tip = landmark_coords[4]
            index_tip = landmark_coords[8]
            middle_tip = landmark_coords[12]
            ring_tip = landmark_coords[16]
            pinky_tip = landmark_coords[20]

            # Example: Calculate vector from index fingertip to middle fingertip
            index_to_middle = (middle_tip[0] - index_tip[0], middle_tip[1] - index_tip[1])

            # Example: Calculate angle of orientation for index finger (in degrees)
            index_orientation = round((180 / 3.14159) * (atan2(index_to_middle[1], index_to_middle[0])), 2)

            # Get finger direction
            index_direction = get_finger_direction(index_orientation)

            # Display finger direction (example: index finger)
            cv2.putText(frame, f"Index direction: {index_direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)
            print(index_direction)

            if index_direction == "Right":
                Controller().press(Key.right)
                time.sleep(0.1)
            elif index_direction == "Left":
                Controller().press(Key.left)
                time.sleep(0.1)
            elif index_direction == "Up":
                Controller().press(Key.up)
                time.sleep(0.1)
            elif index_direction == "Down":
                Controller().press(Key.down)
                time.sleep(0.1)
            else:
                continue
                time.sleep(1)

    # Display the frame
    cv2.imshow('Finger Direction Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
