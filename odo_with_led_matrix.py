import cv2
import numpy as np
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# Set up LED matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0)
device.contrast(0x0f)
device.clear()

# Set up camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Set up parameters for optical flow
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Initialize variables
prev_gray = None
prev_corners = None

px_per_m = 30  # pixels per meter
disp_thresh = 0.1  # displacement threshold in meters

while True:
    # Capture frame from camera
    ret, frame = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is not None:
        # Calculate optical flow
        displacement, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_corners, None, **lk_params)
        good_new = displacement[status == 1]
        good_old = prev_corners[status == 1]

        # Calculate mean displacement and direction
        mean_disp = np.mean(good_new - good_old, axis=0)
        disp_norm = np.linalg.norm(mean_disp)

        # Draw optical flow on frame and display on LED matrix
        frame_flow = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        if disp_norm > disp_thresh:
            # Calculate distance in pixels and convert to meters
            dist_pix = np.linalg.norm(mean_disp) / px_per_m
            if dist_pix >= 0:
                cv2.arrowedLine(frame_flow, (int(prev_corners[0][0]), int(prev_corners[0][1])),
                                (int(prev_corners[0][0] + mean_disp[0]), int(prev_corners[0][1] + mean_disp[1])),
                                (0, 0, 255), 2, cv2.LINE_AA)
                if mean_disp[0] > 0:
                    with canvas(device) as draw:
                        draw.polygon([(0, 0), (7, 0), (3, 3)], fill='white')
                elif mean_disp[0] < 0:
                    with canvas(device) as draw:
                        draw.polygon([(0, 0), (0, 7), (3, 3)], fill='white')
                if mean_disp[1] > 0:
                    with canvas(device) as draw:
                        draw.polygon([(0, 0), (0, 3), (3, 3)], fill='white')
                elif mean_disp[1] < 0:
                    with canvas(device) as draw:
                        draw.polygon([(0, 4), (0, 7), (3, 3)], fill='white')
                device.flush()
            prev_corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
        else:
            prev_corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

        prev_gray = gray

    # Display frame with optical flow
    cv2.imshow('frame', frame_flow)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release camera and close window
cap.release()
cv2.destroyAllWindows()

