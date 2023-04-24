import cv2
import numpy as np

# Initialize the camera and set the resolution
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

# Create a blank map with a white background
map_size2 = (1600, 1200)
map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255

# Initialize the previous image and the initial position
prev_img = None
pos = [map_size2[0] // 2, map_size2[1] // 2]
pos_history = []

# Draw a grid on the map
grid_size = 2
#for i in range(grid_size, map_size[0], grid_size):
 #   cv2.line(map_img, (i, 0), (i, map_size[1]), (128, 128, 128), 5)
#for j in range(grid_size, map_size[1], grid_size):
 #   cv2.line(map_img, (0, j), (map_size[0], j), (128, 128, 128), 5)

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
        pos[0] -= int(avg_flow_x)
        pos[1] -= int(avg_flow_y)

        # Add the current position to the history
        pos_history.append(tuple(pos))

        # Draw the position history on the map
        map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255
        for i in range(grid_size, map_size2[0], grid_size):
            cv2.line(map_img, (i, 0), (i, map_size2[1]), (128, 128, 128), 10)
        for j in range(grid_size, map_size2[1], grid_size):
            cv2.line(map_img, (0, j), (map_size2[0], j), (128, 128, 128), 10)

        for i in range(1, len(pos_history)):
            cv2.line(map_img, pos_history[i - 1], pos_history[i], (0, 0, 0), 15)

        # Draw the current position on the map
        cv2.rectangle(map_img, (pos[0]-30, pos[1]-30), (pos[0]+30, pos[1]+30), (255, 0, 0), -1)
        cv2.rectangle(map_img, (pos[0]-20, pos[1]-20), (pos[0]+20, pos[1]+20), (0, 0, 255), -1)
        #cv2.putText(map_img,'Pi', pos[0],pos[1], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Resize the map to 1/10th of the original size for display
        display_size = (int(map_size2[0] / 5), int(map_size2[1] / 5))
        map_display = cv2.resize(map_img, display_size)

        # Display the map
        cv2.imshow('map', map_display)

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
