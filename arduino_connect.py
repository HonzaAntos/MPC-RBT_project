# works great with 27900000px/m...small error
# spi communication with arduino, that sends x,y accumulated position
# communication over USB0 (9600bd)
import serial
import numpy as np
import cv2
import RPi.GPIO as GPIO

# initialize camera
cap = cv2.VideoCapture(0) # assuming camera is connected to the Pi's USB port
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with the name of your serial port

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# Turn on the LED strips
GPIO.output(18, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)
GPIO.output(14, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)

# initialize previous frame and previous keypoints
prev_frame = None
prev_pts = None

# initialize x and y distances traveled
x_distance = 0
y_distance = 0

# Create a blank map with a white background
map_size2 = (800, 600)
map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255

# Initialize the previous image and the initial position
prev_img = None
pos = [map_size2[0] *5, map_size2[1] *5]
posdiv = [map_size2[0] * 5, map_size2[1] * 5]
pos_history = []

# Initialize plot data pimorono
x_data = []
y_data = []

pospim = [map_size2[0] *5, map_size2[1] *5]

# Initialize circle data
circle_center = None

# Draw a grid on the map
grid_size = 100

# initialize cumulative displacement vector
cumulative_disp = np.array([0, 0], dtype=np.float64)

# initialize font for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# calibration to set 1m in px
meter_in_px = 27900000
#-----------------------------

def get_motion():
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with the name of your serial port
    while True:
        data = ser.readline().decode().strip().split(",")
        value1 = int(data[0])
        value2 = int(data[1])
        return value1, value2

while True:
    # read current frame
    ret, frame = cap.read()
    if not ret:
        break

    # Read data from arduino
    x,y = get_motion()

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # compute optical flow if previous frame exists
    if prev_frame is not None:
        # calculate optical flow using Farneback algorithm
        flow = cv2.calcOpticalFlowFarneback(prev_frame, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # integrate flow vectors to obtain displacement vectors
        displacement = np.abs(np.sum(flow, axis=(0, 1))) # To calculate traveled distance, not distance from center
       # x_displacement = displacement[0]
       # y_displacement = displacement[1]

        # update x and y distances traveled
       # x_distance += np.abs(x_displacement)
       # y_distance += np.abs(y_displacement)

        # update cumulative displacement vector
        cumulative_disp = np.add(cumulative_disp, displacement)

        # draw optical flow vectors on screen
        #hsv = np.zeros_like(frame)
       # hsv[..., 1] = 255
       # mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
       # hsv[..., 0] = ang*180/np.pi/2
      #  hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
      #  bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
      #  frame = cv2.addWeighted(frame, 1, bgr, 2, 0)

        # Compute the average motion in x and y direction
        avg_flow_x = (np.mean(flow[:, :, 0]))
        avg_flow_y = (np.mean(flow[:, :, 1]))

        # Update the position estimate
        pos[0] -= int(avg_flow_x)
        pos[1] -= int(avg_flow_y)
        #print("pos 1:", pos[0])
        #print("pos 2:", pos[1])

        # Update the position estimate
        posdiv[0] = (pos[0]//10)
        posdiv[1] = (pos[1]//10)
        #print("pos after div 1:", posdiv[0])
        #print("pos after div 2:", (posdiv[1]))

        # Add the current position to the history
        pos_history.append(tuple(posdiv))

        # Draw the position history on the map
        map_img = np.ones((map_size2[1], map_size2[0], 3), np.uint8) * 255
      #  for i in range(grid_size, map_size2[0], grid_size):
       #     cv2.line(map_img, (i, 0), (i, map_size2[1]), (128, 128, 128), 1)
      #  for j in range(grid_size, map_size2[1], grid_size):
      #      cv2.line(map_img, (0, j), (map_size2[0], j), (128, 128, 128), 1)
        for i in range(1, len(pos_history)):
            cv2.line(map_img, pos_history[i - 1], pos_history[i], (0, 0, 0), 5)

        # Draw the current position on the map
        cv2.rectangle(map_img, (posdiv[0] - 30, posdiv[1] - 30), (posdiv[0] + 30, posdiv[1] + 30), (255, 0, 0), -1)
       # cv2.rectangle(map_img, (posdiv[0] - 20, posdiv[1] - 20), (posdiv[0] + 20, posdiv[1] + 20), (0, 0, 255), -1)

        # Resize the map to 1/10th of the original size for display
        display_size = (int(map_size2[0] / 2), int(map_size2[1] / 2))
        map_display = cv2.resize(map_img, display_size)

        # display distance traveled on screen
        distance = np.sqrt((cumulative_disp[0])**2 + (cumulative_disp[1])**2)
        distance_in_m = (distance/meter_in_px)
        #cv2.putText(frame, f": {distance_in_m:.2f} meters", (10, 30), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(map_display, f": {distance_in_m:.2f} meters", (10, 30), font,1, (0, 255, 0), 2, cv2.LINE_AA)

        # Pimoroni code
        pospim[0] += x
        pospim[1] -= y
        print("Relative: x {:03d} y {:03d} | Absolute: x {:03d} y {:03d}".format(x, y, pospim[0], pospim[1]))

        # Update plot data
        x_data.append(pospim[0])
        y_data.append(pospim[1])

        dx, dy = get_motion()  # Read motion data from sensor
        x, y = x_data[-1] + dx, y_data[-1] + dy  # Calculate new position
        # Draw all previous position on the map
        for i in range(len(x_data) - 1):
            cv2.line(map_display, (x_data[i], y_data[i]), (x_data[i + 1], y_data[i + 1]), (255, 0, 0), thickness=(20))

        # Draw the current position on the map
        if len(x_data) > 0:
            new_circle_center = (int(x_data[-1]), int(y_data[-1]))

            # Remove previous circle
            if circle_center is not None:
                cv2.circle(map_display, circle_center, 50, (255, 255, 255), thickness=20)
                print("in if circle center is none")

            # Draw new circle
            cv2.circle(map_display, new_circle_center, 50, (0, 255, 0), thickness=20)
            cv2.circle(map_display, new_circle_center, 50, (0, 0, 255), thickness=10)

            circle_center = new_circle_center

        # Display the map
        cv2.imshow('map', map_display)

    # update previous frame and previous keypoints
    prev_frame = gray.copy()

    # Resize the map to 1/10th of the original size for display
    display_size = (320, 240)
    map_display = cv2.resize(frame, display_size)

    # display frame with optical flow and distance traveled
    #cv2.imshow('frame', map_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cap.release()
cv2.destroyAllWindows()
# Turn off the LED strips
GPIO.output(18, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(14, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
# Clean up the GPIO pins
GPIO.cleanup()

#171516680px =~ 1m
#164502000px =~1m -> correct value for 320x240 resolution
