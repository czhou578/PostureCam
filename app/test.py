import cv2
import mediapipe as mp
import numpy as np

print("OpenCV version:", cv2.__version__)
print("MediaPipe version:", mp.__version__)

cv2.imshow("Test", np.zeros((300, 300, 3), dtype=np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
