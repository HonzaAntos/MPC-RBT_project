# works great with 27900000px/m...small error

import numpy as np
import cv2
import RPi.GPIO as GPIO

# initialize camera
cap = cv2.VideoCapture(0) # assuming camera is connected to the Pi's USB port
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

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

# initialize cumulative displacement vector
cumulative_disp = np.array([0, 0], dtype=np.float64)

# initialize font for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# calibration to set 1m in px
meter_in_px = 27900000
while True:
    # read current frame
    ret, frame = cap.read()
    if not ret:
        break

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # compute optical flow if previous frame exists
    if prev_frame is not None:
        # calculate optical flow using Farneback algorithm
        flow = cv2.calcOpticalFlowFarneback(prev_frame, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # integrate flow vectors to obtain displacement vectors
        displacement = np.sum(flow, axis=(0, 1))
        x_displacement = displacement[0]
        y_displacement = displacement[1]

        # update x and y distances traveled
        x_distance += x_displacement
        y_distance += y_displacement

        # update cumulative displacement vector
        cumulative_disp = np.add(cumulative_disp, displacement)

        # draw optical flow vectors on screen
        hsv = np.zeros_like(frame)
        hsv[..., 1] = 255
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang*180/np.pi/2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        frame = cv2.addWeighted(frame, 1, bgr, 2, 0)

        # display distance traveled on screen
        distance = np.sqrt((cumulative_disp[0])**2 + (cumulative_disp[1])**2)
        distance_in_m = (distance/meter_in_px)
        cv2.putText(frame, f": {distance_in_m:.2f} meters", (10, 30), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    # update previous frame and previous keypoints
    prev_frame = gray.copy()

    # Resize the map to 1/10th of the original size for display
    display_size = (640, 480)
    map_display = cv2.resize(frame, display_size)

    # display frame with optical flow and distance traveled
    cv2.imshow('frame', map_display)
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