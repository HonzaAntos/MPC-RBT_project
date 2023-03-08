import cv2
import numpy as np

# Initialize camera object
cap = cv2.VideoCapture(0)

# Set parameters for Shi-Tomasi corner detection
feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

# Set parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Initialize variables
prev_frame = None
prev_corners = None
prev_gray = None
cur_frame = None
cur_gray = None
cur_corners = None
R = np.eye(3)
T = np.zeros((3, 1))

while True:
    # Capture current frame
    ret, cur_frame = cap.read()

    # Convert current frame to grayscale
    cur_gray = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)

    if prev_frame is not None:
        # Calculate optical flow using previous and current frames
        cur_corners, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, cur_gray, prev_corners, None, **lk_params)

        # Select good points
        good_new = cur_corners[status == 1]
        good_old = prev_corners[status == 1]

        # Estimate the Essential matrix using RANSAC
        E, mask = cv2.findEssentialMat(good_new, good_old, focal=1.0, pp=(0, 0), method=cv2.RANSAC, prob=0.999, threshold=1.0)

        # Recover the rotation and translation matrices from the Essential matrix
        _, R, T, _ = cv2.recoverPose(E, good_new, good_old)

        # Accumulate rotation and translation over time
        R = R.dot(R)
        T = T + R.dot(T)

        # Display camera pose
        print("Rotation matrix: ")
        print(R)
        print("Translation vector: ")
        print(T)

    # Store current frame and corners as previous for next iteration
    prev_frame = cur_frame.copy()
    prev_gray = cur_gray.copy()
    prev_corners = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

    # Display current frame
    cv2.imshow("Frame", cur_frame)

    # Wait for user input to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
