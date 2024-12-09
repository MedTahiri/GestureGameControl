import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb_frame)

    if results.pose_landmarks:

        landmark_coords = [(int(l.x * frame.shape[1]), int(l.y * frame.shape[0])) for l in results.pose_landmarks.landmark]

        height, width, _ = frame.shape

        zone1_end = width // 2

        zone2_end = height//2

        cv2.line(frame, (zone1_end, 0), (zone1_end, height), (0, 255, 0), 2)
        cv2.line(frame, (0, zone2_end), (width, zone2_end), (0, 255, 0), 2)

        head_y = landmark_coords[mp_pose.PoseLandmark.RIGHT_INDEX.value][1]

        head_x = landmark_coords[mp_pose.PoseLandmark.RIGHT_INDEX.value][0]

        if  head_y > zone2_end :
            print("up")
        elif  head_y < zone2_end :
            print("down")

        if head_x < zone1_end:
            print("left")
        elif head_x > zone1_end:
            print("right")

    cv2.imshow('Jump Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
