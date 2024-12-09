import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize variables for tracking previous position
prev_head_y = 0
prev_head_x = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect pose
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Get landmark coordinates
        landmark_coords = [(int(l.x * frame.shape[1]), int(l.y * frame.shape[0])) for l in results.pose_landmarks.landmark]

        # Get position of head (for example)
        head_y = landmark_coords[mp_pose.PoseLandmark.NOSE.value][1]

        head_x = landmark_coords[mp_pose.PoseLandmark.NOSE.value][0]

        # Calculate vertical movement
        vertical_movement = head_y - prev_head_y

        horizontal_movement = head_x - prev_head_x

        # Update previous position
        prev_head_y = head_y
        prev_head_x = head_x

        # Detect jumping (example: vertical movement exceeds threshold)
        jump_threshold = 20  # Adjust as needed
        if vertical_movement > jump_threshold:
            print("Jump detected!")
        if horizontal_movement > 0:
            print("go to Left")
        elif horizontal_movement < 0:
            print("go to Right")

        # Draw landmarks on image
        for landmark_coord in landmark_coords:
            cv2.circle(frame, landmark_coord, 5, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow('Jump Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
