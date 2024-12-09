import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

keyboard = Controller()

left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from webcam. Exiting...")
        break
    height, width, _ = frame.shape

    # Calculate zone boundaries
    zone1_end = width // 3
    zone2_end = 2 * width // 3

    # Draw zone boundaries on the frame
    cv2.line(frame, (zone1_end, 0), (zone1_end, height), (0, 0, 0), 2)
    cv2.line(frame, (zone2_end, 0), (zone2_end, height), (0, 0, 0), 2)

    zone3_end = height // 3
    zone4_end = 2 * height // 3

    # Draw zone boundaries on the frame
    cv2.line(frame, (0, zone3_end), (width, zone3_end), (0, 0, 0), 2)
    cv2.line(frame, (0, zone4_end), (width, zone4_end), (0, 0, 0), 2)

    # Convert the BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands.
    results = hands.process(rgb_frame)

    # Reset key presses.
    left_pressed = False
    right_pressed = False
    up_pressed = False
    down_pressed = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            x_center = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
            y_center = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])

            if x_center > 2 * frame.shape[1] // 3:
                position_text = "Left"
                if not left_pressed:
                    keyboard.press(Key.left)
                    left_pressed = True
            elif x_center < 2 * frame.shape[1] // 3 and x_center > frame.shape[1] // 3:
                left_pressed = False
                right_pressed = False
            else:
                position_text = "Right"
                if not right_pressed:
                    keyboard.press(Key.right)
                    right_pressed = True

            if y_center > 2 * frame.shape[0] // 3:
                position_text = "Down"
                if not down_pressed:
                    keyboard.press(Key.down)
                    down_pressed = True
            elif y_center < 2 * frame.shape[0] // 3 and y_center > frame.shape[0] // 3:
                up_pressed = False
                down_pressed = False
            else:
                position_text = "Up"
                if not up_pressed:
                    keyboard.press(Key.up)
                    up_pressed = True

    cv2.imshow('Hand Position', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if not left_pressed:
        keyboard.release(Key.left)
    if not right_pressed:
        keyboard.release(Key.right)
    if not up_pressed:
        keyboard.release(Key.up)
    if not down_pressed:
        keyboard.release(Key.down)

cap.release()
cv2.destroyAllWindows()
