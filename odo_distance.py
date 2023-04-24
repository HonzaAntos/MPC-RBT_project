import cv2
import numpy as np

# Initialize variables
previous_x, previous_y = None, None
positions = []

# Initialize map image
map_size = (800, 600)
map_image = np.zeros((map_size[1], map_size[0], 3), np.uint8)

# Draw grid on map
cell_size = 50
for x in range(0, map_size[0], cell_size):
    cv2.line(map_image, (x, 0), (x, map_size[1]), (128, 128, 128), 1)
for y in range(0, map_size[1], cell_size):
    cv2.line(map_image, (0, y), (map_size[0], y), (128, 128, 128), 1)

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a blur to the grayscale image
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # Detect edges in the blurred image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours in the edges image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the largest area
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        moment = cv2.moments(max_contour)
        if moment["m00"] > 0:
            # Calculate the center of the contour
            cx = int(moment["m10"] / moment["m00"])
            cy = int(moment["m01"] / moment["m00"])

            # Draw a rectangle around the contour
            cv2.rectangle(frame, (cx - 30, cy - 30), (cx + 30, cy + 30), (0, 255, 0), 2)

            # Calculate the distance between the previous and current positions
            if previous_x is not None and previous_y is not None:
                distance = np.sqrt((cx - previous_x) ** 2 + (cy - previous_y) ** 2)
                positions.append((cx, cy))

                # Draw a line between the previous and current positions
                for i in range(1, len(positions)):
                    cv2.line(map_image, positions[i - 1], positions[i], (255, 0, 0), 2)

                # Print the distance on the frame
                cv2.putText(frame, f"Distance: {distance:.2f} pixels", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 0, 255), 2)

            # Update the previous position
            previous_x, previous_y = cx, cy

    # Show the frame and the map
    cv2.imshow("Frame", frame)
    cv2.imshow("Map", map_image)

    # Stop the program when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
