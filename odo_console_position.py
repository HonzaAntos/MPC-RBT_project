import cv2
import numpy as np

# Initialize the camera and set the resolution
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Initialize the previous image and the initial position
prev_img = None
pos = [0, 0]

while True:
    # Capture a new frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Compute the optical flow
    if prev_img is not None:
        flow = cv2.calcOpticalFlowFarneback(prev_img, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Compute the average motion in x and y direction
        avg_flow_x = np.mean(flow[:, :, 0])
        avg_flow_y = np.mean(flow[:, :, 1])


        # Update the position estimate
        pos[0] += avg_flow_x
        pos[1] += avg_flow_y

        # Print the current position estimate
        print("Position: ({:.2f}, {:.2f})".format(pos[0], pos[1]))

    # Display the current frame
    cv2.imshow('frame', frame)

    # Update the previous image
    prev_img = gray

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
