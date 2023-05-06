import serial
import numpy as np
import cv2
import math
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with the name of your serial port
meter_in_px = 10000

# Create a blank map with a white background
map_size2 = (800, 600)
map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255
pos = [map_size2[0] *5, map_size2[1] *5]
posdiv = [map_size2[0] * 5, map_size2[1] * 5]
pos_history = []

# Initialize plot data pimorono
x_data = []
y_data = []

dx = 0
dy = 0

# initialize font for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# Draw a grid on the map
grid_size = 200

while True:
    data = ser.readline().decode().strip().split(",")
    x = int(data[0])
    y = int(data[1])
    delta_x=int(data[2])
    delta_y=int(data[3])
    distance_arduino= int(data[4])
    print("x:", x)
    print("y:", y)
    print("dx:", delta_x)
    print("dy:", delta_y)

    # Calculate traveled distance
    dx+=np.abs(delta_x)
    dy+=np.abs(delta_y)
    travel_distance=np.abs(np.sqrt((dx)**2 + (dy)**2))
    print("traveled:", travel_distance)

    # Scale position to map ...divide by 10
    posdiv[0] = ((x//50)+pos[0]//10)
    posdiv[1] = ((y//50)+pos[1]//10)
    print("xpos:", posdiv[0])
    print("ypos:", posdiv[1])
    # Add the current position to the history
    pos_history.append(tuple(posdiv))

    # Draw the position history on the map
    map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255
    for i in range(grid_size, map_size2[0], grid_size):
        cv2.line(map_img, (i, 0), (i, map_size2[1]), (128, 128, 128), 1)
    for j in range(grid_size, map_size2[1], grid_size):
       cv2.line(map_img, (0, j), (map_size2[0], j), (128, 128, 128), 1)
    for i in range(1, len(pos_history)):
        cv2.line(map_img, pos_history[i - 1], pos_history[i], (0, 0, 0), 5)
        # Draw the current position on the map
        cv2.rectangle(map_img, (posdiv[0] - 20, posdiv[1] - 20), (posdiv[0] + 20, posdiv[1] + 20), (255, 0, 0), -1)
        cv2.rectangle(map_img, (posdiv[0] - 15, posdiv[1] - 15), (posdiv[0] + 15, posdiv[1] + 15), (0, 0, 255), -1)

    # display distance traveled on screen
    distance_from_start = np.sqrt((x)**2 + (y)**2)
    distance_in_m = (travel_distance/meter_in_px)
    distance_from_start_m = (distance_arduino/meter_in_px)
    cv2.putText(map_img, f": {distance_in_m:.2f} m traveled", (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(map_img, f": {distance_from_start_m:.2f} m from start", (10, 80), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Resize the map to 1/10th of the original size for display
    display_size = (int(map_size2[0] / 2), int(map_size2[1] / 2))
    map_display = cv2.resize(map_img, display_size)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the map
    cv2.imshow('map', map_display)

# release resources
cv2.destroyAllWindows()
