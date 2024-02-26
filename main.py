import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import tkinter as tk
from PIL import ImageTk, Image
from cvzone.HandTrackingModule import HandDetector

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

keyboard = Controller()

left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
wCam, hCam = 640, 480

detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

cap = None
is_recognizing = False
previous_gestures = 0


def open_camera1():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
        button1.config(state="disabled")
        button2.config(state="normal")
        update_frame1()


def close_camera1():
    global cap
    if cap is not None and cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
        button1.config(state="normal")
        button2.config(state="disabled")


def update_frame1():
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            height, width, _ = frame.shape

            zone1_end = width // 3
            zone2_end = 2 * width // 3

            cv2.line(frame, (zone1_end, 0), (zone1_end, height), (0, 0, 0), 2)
            cv2.line(frame, (zone2_end, 0), (zone2_end, height), (0, 0, 0), 2)

            zone3_end = height // 3
            zone4_end = 2 * height // 3

            cv2.line(frame, (0, zone3_end), (width, zone3_end), (0, 0, 0), 2)
            cv2.line(frame, (0, zone4_end), (width, zone4_end), (0, 0, 0), 2)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb_frame)

            global left_pressed, right_pressed, up_pressed, down_pressed
            left_pressed = False
            right_pressed = False
            up_pressed = False
            down_pressed = False

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    x_center = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
                    y_center = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])

                    if x_center > 2 * frame.shape[1] // 3:
                        if not left_pressed:
                            keyboard.press(Key.left)
                            left_pressed = True
                    elif x_center < 2 * frame.shape[1] // 3 and x_center > frame.shape[1] // 3:
                        left_pressed = False
                        right_pressed = False
                    else:
                        if not right_pressed:
                            keyboard.press(Key.right)
                            right_pressed = True

                    if y_center > 2 * frame.shape[0] // 3:
                        if not down_pressed:
                            keyboard.press(Key.down)
                            down_pressed = True
                    elif y_center < 2 * frame.shape[0] // 3 and y_center > frame.shape[0] // 3:
                        up_pressed = False
                        down_pressed = False
                    else:
                        if not up_pressed:
                            keyboard.press(Key.up)
                            up_pressed = True
            cv2.imshow('Hand Position', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                return
            if not left_pressed:
                keyboard.release(Key.left)
            if not right_pressed:
                keyboard.release(Key.right)
            if not up_pressed:
                keyboard.release(Key.up)
            if not down_pressed:
                keyboard.release(Key.down)
            root.after(10, update_frame1)
        else:
            root.after(10, update_frame1)
    else:
        print("camera 1 was closed")
        pass


def open_camera2():
    global cap, is_recognizing
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    is_recognizing = True
    button3.config(state="disabled")
    button4.config(state="normal")
    update_frame2()


def close_camera2():
    global cap, is_recognizing
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        is_recognizing = False
        button3.config(state="normal")
        button4.config(state="disabled")


def update_frame2():
    if is_recognizing:
        success, img = cap.read()

        hands, img = detector.findHands(img, draw=True, flipType=True)
        fingers1 = []
        fingers2 = []

        if hands:
            hand1 = hands[0]
            lmList1 = hand1["lmList"]
            fingers1 = detector.fingersUp(hand1)

            if len(hands) == 2:
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                fingers2 = detector.fingersUp(hand2)

            gestures = fingers1.count(1) + fingers2.count(1)
            if gestures == 5:
                keyboard.press(Key.up)
            elif gestures == 0:
                keyboard.press(Key.down)
            elif gestures == 10:
                keyboard.press(Key.space)
                keyboard.release(Key.space)
                keyboard.press(Key.down)
                keyboard.release(Key.down)
            elif gestures == 1:
                keyboard.press(Key.left)
            elif gestures == 4:
                keyboard.press(Key.right)
            else:
                if previous_gestures == 5:
                    keyboard.release(Key.up)
                elif previous_gestures == 0:
                    keyboard.release(Key.down)
                elif previous_gestures == 1:
                    keyboard.release(Key.left)
                elif previous_gestures == 4:
                    keyboard.release(Key.right)

            previous_gestures = gestures
        else:
            print("camera 2 was closed")

        cv2.imshow("Finger count", img)
        cv2.waitKey(1)
        root.after(10, update_frame2)


root = tk.Tk()
root.title("INSEA INNOVATION EDGE")

root.geometry("600x500")

image_path = "iie.png"
image = Image.open(image_path)
image = image.resize((200, 200))
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

text_label = tk.Label(root, text="festival des sciences de rabat", font=("Helvetica", 12))
text_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

title1_label = tk.Label(root, text="Control by Hand", font=("Helvetica", 12))
title1_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))
button1 = tk.Button(root, text="Start", width=15, command=open_camera1)
button1.grid(row=3, column=0, padx=10, pady=10)

button2 = tk.Button(root, text="Stop", width=15, command=close_camera1, state="disabled")
button2.grid(row=3, column=1, padx=10, pady=10)

title2_label = tk.Label(root, text="Control by finger", font=("Helvetica", 12))
title2_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

button3 = tk.Button(root, text="Start", width=15, command=open_camera2)
button3.grid(row=5, column=0, padx=10, pady=10)

button4 = tk.Button(root, text="Stop", width=15, command=close_camera2, state="disabled")
button4.grid(row=5, column=1, padx=10, pady=10)

for child in root.winfo_children():
    child.grid_configure(padx=10, pady=10, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
