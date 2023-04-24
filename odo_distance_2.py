import cv2
import numpy as np

# initialize the camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Create a blank map with a white background
map_size2 = (3400, 2400)
map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255

# initialize the previous frame
prev_frame = None
pos = [map_size2[0] // 2, map_size2[1] // 2]
pos_history = []

# Draw a grid on the map
grid_size = 20

# initialize the current position and distance traveled
x = 160
y = 120
distance_traveled = 0

# create empty list to store previous positions
positions = []

while True:
    # read the current frame
    ret, frame = camera.read()
    if not ret:
        break

    # convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_frame is not None:
        # calculate the optical flow
        flow = cv2.calcOpticalFlowFarneback(prev_frame, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # get the average flow direction
        flow_avg = np.mean(flow, axis=(0,1))
        flow_x = flow_avg[0]
        flow_y = flow_avg[1]

        # Update the position estimate
        pos[0] -= int(flow_x)
        pos[1] -= int(flow_y)

        # Add the current position to the history
        pos_history.append(tuple(pos))

        # Draw the position history on the map
        map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255
        for i in range(grid_size, map_size2[0], grid_size):
            cv2.line(map_img, (i, 0), (i, map_size2[1]), (128, 128, 128), 1)
        for j in range(grid_size, map_size2[1], grid_size):
            cv2.line(map_img, (0, j), (map_size2[0], j), (128, 128, 128), 1)

        for i in range(1, len(pos_history)):
            cv2.line(map_img, pos_history[i - 1], pos_history[i], (0, 0, 0), 5)

        # Draw the current position on the map
        cv2.rectangle(map_img, (pos[0] - 30, pos[1] - 30), (pos[0] + 30, pos[1] + 30), (255, 0, 0), -1)
        cv2.rectangle(map_img, (pos[0] - 2, pos[1] - 2), (pos[0] + 2, pos[1] + 2), (0, 0, 255), -1)

        # Resize the map to 1/10th of the original size for display
        display_size = (int(map_size2[0] / 10), int(map_size2[1] / 10))
        map_display = cv2.resize(map_img, display_size)

        # Display the map
        cv2.imshow('map', map_display)

        # move to new position
        x_new = x + int(flow_x)
        y_new = y + int(flow_y)

        # check if out of bounds
        #if x_new < 0 or x_new >= 320 or y_new < 0 or y_new >= 240:
            #break

        # calculate distance traveled and update total distance
        distance = np.sqrt((x_new - x)**2 + (y_new - y)**2)
        distance_traveled += distance

        # update current position
        x = x_new
        y = y_new

        # draw current position on frame
        cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)

        # add current position to list of previous positions
        positions.append((x, y))

        # draw previous positions on frame as a line
        for i in range(len(positions) - 1):
            cv2.line(frame, positions[i], positions[i+1], (0, 255, 0), 2)

    # display the frame and distance traveled
    cv2.putText(frame, f"Distance Traveled: {distance_traveled:.2f} pixels", (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

    # update the previous frame
    prev_frame = gray.copy()

# release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
