import cv2
import mediapipe as mp
import math

def calculate_angle(point1, point2):
    return math.degrees(math.atan2(point2.y - point1.y, point2.x - point1.x))

if results.pose_landmarks:
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    mid_spine = landmarks[mp_pose.PoseLandmark.LEFT_HIP]  # Example

    # Calculate angle
    spine_angle = calculate_angle(left_shoulder, mid_spine)
    print(f"Spine Angle: {spine_angle}")

    # Check if slouching
    if spine_angle < 80:  # Example threshold
        print("Slouching detected!")

# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Use Pose with default parameters
with mp_pose.Pose(static_image_mode=False,
                  model_complexity=1,
                  enable_segmentation=False,
                  min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB (MediaPipe works with RGB)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image to detect pose
        results = pose.process(image)

        # Draw pose landmarks on the original frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the frame with landmarks
        cv2.imshow('MediaPipe Pose', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
