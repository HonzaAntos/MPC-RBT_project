#!/usr/bin/env python
import time
import argparse
from pmw3901 import PMW3901, PAA5100, BG_CS_FRONT_BCM, BG_CS_BACK_BCM
import numpy as np
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--board', type=str,
                    choices=['pmw3901', 'paa5100'],
                    help='Breakout type.')
parser.add_argument('--rotation', type=int,
                    default=0, choices=[0, 90, 180, 270],
                    help='Rotation of sensor in degrees.')
parser.add_argument('--spi-slot', type=str,
                    default='front', choices=['front', 'back'],
                    help='Breakout Garden SPI slot.')

args = parser.parse_args()

# Define map size and scale
map_size = (5000, 5000)  # Map size in pixels
map_scale = 0.1  # Scale of map in pixels per mm
map_multiplier = 1/map_scale
# Initialize map image
map_image = 255 * np.ones((map_size[1], map_size[0], 3), dtype=np.uint8)

# Pick the right class for the specified breakout
SensorClass = PMW3901 if args.board == 'pmw3901' else PAA5100

flo = SensorClass(spi_port=0, spi_cs_gpio=BG_CS_FRONT_BCM if args.spi_slot == 'front' else BG_CS_BACK_BCM)
flo.set_rotation(args.rotation)

tx = 0
ty = 0
# Initialize plot data
x_data = []
y_data = []

pos = [map_size[0] // 2, map_size[1] // 2]

# Initialize circle data
circle_center = None

# Draw a grid on the map
grid_size = 200
# Draw path on map image
for i in range(grid_size, map_size[0], grid_size):
    cv2.line(map_image, (i, 0), (i, map_size[1]), (128, 128, 128), 10)
for j in range(grid_size, map_size[1], grid_size):
    cv2.line(map_image, (0, j), (map_size[0], j), (128, 128, 128), 10)

try:
    while True:
        try:
            x, y = flo.get_motion()
        except RuntimeError:
            continue
        pos[0] += x
        pos[1] -= y
        print("Relative: x {:03d} y {:03d} | Absolute: x {:03d} y {:03d}".format(x, y, pos[0], pos[1]))

        # Update plot data
        x_data.append(pos[0])
        y_data.append(pos[1])

        dx, dy = flo.get_motion()  # Read motion data from sensor
        x, y = x_data[-1] + dx, y_data[-1] + dy  # Calculate new position

        # Draw all previous position on the map
        for i in range(len(x_data) - 1):
            cv2.line(map_image, (x_data[i], y_data[i]), (x_data[i + 1], y_data[i + 1]), (0, 0, 0), thickness=(20))

        # Draw the current position on the map
        if len(x_data) > 0:
            new_circle_center = (int(x_data[-1] ), int(y_data[-1]))

            # Remove previous circle
            if circle_center is not None:
                cv2.circle(map_image, circle_center, 5, (255, 255, 255), thickness=200)
                print("in if circle center is none")

            # Draw new circle
            cv2.circle(map_image, new_circle_center, 5, (0, 255, 0), thickness=200)
            cv2.circle(map_image, new_circle_center, 5, (0, 0, 255), thickness=100)

            circle_center = new_circle_center

        # Resize matrix on map
        display_size = (int(map_size[0] / 10), int(map_size[1] / 10))
        map_display = cv2.resize(map_image, display_size)


        # Display map image
        cv2.imshow("Map", map_display)
        cv2.waitKey(1)

except KeyboardInterrupt:
    pass