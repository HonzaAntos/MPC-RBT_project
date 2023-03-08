import picamera
from time import sleep


# Initialize the camera
camera = picamera.PiCamera()

# Set camera resolution (optional)
camera.resolution = (640, 480)

# Start the preview
camera.start_preview()

# Wait for the camera to warm up
sleep(2)

# Capture an image and save it to file
camera.capture('/home/pi/image.jpg')

# Stop the preview and release the camera resources
camera.stop_preview()
camera.close()
