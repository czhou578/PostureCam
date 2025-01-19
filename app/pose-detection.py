import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Get the frame height for relative position calculations
ret, frame = cap.read()
if ret:
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
else:
    frame_height = 480  
    frame_width = 640

# Define calibration variables
calibration_samples = []
CALIBRATION_FRAMES = 30
is_calibrating = True

try:
    with mp_face_detection.FaceDetection(
        model_selection=0,  # 0 for close range, 1 for far range
        min_detection_confidence=0.5
    ) as face_detection:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Convert to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the image
            results = face_detection.process(image)
            
            # Convert back to BGR for display
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.detections:
                for detection in results.detections:
                    # Get bounding box coordinates
                    bbox = detection.location_data.relative_bounding_box
                    
                    # Convert relative coordinates to absolute
                    h = int(bbox.height * frame_height)
                    w = int(bbox.width * frame_width)
                    x = int(bbox.xmin * frame_width)
                    y = int(bbox.ymin * frame_height)
                    
                    # Draw face detection box
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Calculate metrics
                    face_size = (h * w) / (frame_height * frame_width)  # relative face area
                    head_position = y / frame_height  # relative vertical position (0 at top, 1 at bottom)
                    
                    # Calibration phase
                    if is_calibrating:
                        calibration_samples.append((face_size, head_position))
                        cv2.putText(image, f"Calibrating: {len(calibration_samples)}/{CALIBRATION_FRAMES}",
                                  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        if len(calibration_samples) >= CALIBRATION_FRAMES:
                            # Calculate baseline metrics
                            baseline_face_size = sum(s[0] for s in calibration_samples) / len(calibration_samples)
                            baseline_head_pos = sum(s[1] for s in calibration_samples) / len(calibration_samples)
                            is_calibrating = False
                    else:
                        # Check posture based on calibrated values
                        face_size_diff = (face_size - baseline_face_size) / baseline_face_size * 100
                        head_pos_diff = (head_position - baseline_head_pos) / baseline_head_pos * 100
                        
                        # Display metrics
                        cv2.putText(image, f"Face size change: {face_size_diff:.1f}%",
                                  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(image, f"Head position change: {head_pos_diff:.1f}%",
                                  (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Posture warnings
                        if face_size_diff > 20:  # face is 20% larger
                            cv2.putText(image, "Too close to screen!",
                                      (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        
                        if head_pos_diff > 15:  # head is 15% lower
                            cv2.putText(image, "You're slouching!",
                                      (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Display the frame
            cv2.imshow('Posture Detection', image)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    cap.release()
    cv2.destroyAllWindows()