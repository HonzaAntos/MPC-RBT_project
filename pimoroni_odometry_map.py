import cv2
import pmw3901
import numpy as np


# Define sensor parameters
sensor_params = {
    'bus': 0,
    'device': 1,
    'gpio_data': 27,
    'gpio_nreset': 17
}

# Initialize sensor
sensor = pmw3901.PMW3901(**sensor_params)

# Define map size and scale
map_size = (500, 500)  # Map size in pixels

# Initialize map image
map_image = 255 * np.ones((map_size[1], map_size[0], 3), dtype=np.uint8)

# Initialize plot data
x_data = []
y_data = []

# Read odometry data from sensor and update map image
while True:
    dx, dy = sensor.get_motion()  # Read motion data from sensor
    x, y = x_data[-1] + dx, y_data[-1] + dy  # Calculate new position

    # Update plot data
    x_data.append(x)
    y_data.append(y)

    # Draw path on map image
    for i in range(len(x_data) - 1):
        cv2.line(map_image, (x_data[i], y_data[i]), (x_data[i + 1], y_data[i + 1]), (0, 0, 255), thickness=2)

    # Display map image
    cv2.imshow("Map", map_image)
    cv2.waitKey(1)
