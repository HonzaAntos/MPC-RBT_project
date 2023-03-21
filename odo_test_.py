import cv2
import numpy as np

# Initialize the camera and set the resolution
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Create a blank map with a white background
map_size = (640, 480)
map_img = np.ones((map_size[1], map_size[0], 3), np.uint8) * 255

# Initialize the previous image and the initial position
prev_img = None
pos = [map_size[0] // 2, map_size[1] // 2]
pos_history = []

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
        pos[0] += int(avg_flow_x)
        pos[1] += int(avg_flow_y)

        # Add the current position to the history
        pos_history.append(tuple(pos))

        # Draw the position history on the map
        map_img = np.ones((map_size[1], map_size[0], 3), np.uint8) * 255
        for i in range(1, len(pos_history)):
            cv2.line(map_img, pos_history[i - 1], pos_history[i], (0, 0, 0), 2)

        # Draw the current position on the map
        cv2.circle(map_img, tuple(pos), 5, (255, 0, 0), -1)

        # Display the map
        cv2.imshow('map', map_img)

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
