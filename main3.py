import cv2

# Initialize video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Calculate zone boundaries
    zone1_end = width // 3
    zone2_end = 2 * width // 3

    # Draw zone boundaries on the frame
    cv2.line(frame, (zone1_end, 0), (zone1_end, height), (0, 255, 0), 2)
    cv2.line(frame, (zone2_end, 0), (zone2_end, height), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Vertical Zones', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
