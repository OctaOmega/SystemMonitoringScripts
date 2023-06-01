# copyright @ Rajesh Kannan

from PIL import ImageGrab
from base64 import b64encode
from io import BytesIO
from os import system 
from socket import gethostname
from cv2 import VideoCapture, destroyAllWindows, imencode

def screencapture():
    # Capture screenshot
    image = ImageGrab.grab()
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    imageBase64 = b64encode(buffered.getvalue())
    
    return (imageBase64.decode("utf-8"))

def remoteshutdown(timer=60):
    HOST = gethostname()
    message = f"Remote Shutdown Initiated by USOC: You have {timer} Seconds to exit out of any applications"
    command = f'shutdown /s /m \\\\{HOST} /c "{message}" /t {timer}'
    system(command)

def remotewebcam(webview):

    if webview is True:
    # Search for available webcams
        for i in range(10):
            cap = VideoCapture(i)
            if cap.isOpened():
                break

        # If a webcam is found, enable the feed
        if cap.isOpened():
            while True:
                # Capture a frame from the camera
                ret, frame = cap.read()

                # Convert the frame to JPEG format
                if ret:
                    ret, buffer = imencode('.jpg', frame)
                    frameData = buffer.tobytes()
                    frame = buffer.tobytes()
                    # Yield the frame as a response
                    return (yield (  b'--frame\r\n'
                                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'))
    elif webview is False:
        # Release the capture and close the window
        cap.release()
        destroyAllWindows()