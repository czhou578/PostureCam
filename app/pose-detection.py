import cv2
import mediapipe as mp
import math

def find_camera():
    for i in range(10):  # Test indices 0 through 9
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            cap.release()
        else:
            print(f"No camera at index {i}")

def calculate_angle(point1, point2):
    return math.degrees(math.atan2(point2.y - point1.y, point2.x - point1.x))

# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

try:
    # Use Pose with default parameters
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        while True:  # Changed from while cap.isOpened()
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Convert the frame to RGB (MediaPipe works with RGB)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image to detect pose
            results = pose.process(image)

            # Convert back to BGR for display
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw pose landmarks on the frame
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                mid_spine = landmarks[mp_pose.PoseLandmark.LEFT_HIP]

                # Calculate angle
                spine_angle = calculate_angle(left_shoulder, mid_spine)
                print(f"Spine Angle: {spine_angle}")

                # Check if slouching
                if spine_angle < 80:  # Example threshold
                    print("Slouching detected!")
                    cv2.putText(image, "Slouching!", (50, 50),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Display the frame with landmarks
            cv2.imshow('MediaPipe Pose', image)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    # Release resources
    cap.release()
    cv2.destroyAllWindows()