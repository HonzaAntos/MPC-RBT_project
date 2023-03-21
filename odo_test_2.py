import cv2
from picamera import PiCamera
import time

# Initialize the camera
from picamera.array import PiRGBArray

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
time.sleep(2)

# Initialize the OpenCV window
cv2.namedWindow("Frame")

# Define the feature detection method
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Initialize the variables
prev_gray = None
prev_corners = None

# Loop over the frames
while True:
    # Capture a frame
    raw_capture = PiRGBArray(camera, size=(640, 480))
    camera.capture(raw_capture, format="bgr")
    frame = raw_capture.array

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # If this is the first frame, detect features
    if prev_gray is None:
        prev_gray = gray
        prev_corners = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)
    else:
        # Calculate optical flow
        next_corners, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_corners, None, **lk_params)

        # Select good points
        good_old = prev_corners[status == 1]
        good_new = next_corners[status == 1]

        # Calculate the translation and rotation between the frames
        M, mask = cv2.estimateAffinePartial2D(good_old, good_new)

        # Update the previous variables
        prev_gray = gray.copy()
        prev_corners = good_new.reshape(-1, 1, 2)

    # Draw the feature points on the frame
    for corner in prev_corners:
        x, y = corner.ravel()
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # If the q key was pressed, break from the loop
    if key == ord("q"):
        break

# Clean up the camera and close the window
cv2.destroyAllWindows()
camera.close()