import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()
tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()
image_list = []


def video_stream():
    global keepRecording
    global image_list
    
    while keepRecording:
        
        frame = frame_read.frame
        
        if frame is not None and frame.size > 0:
            
            cv2.imshow("Tello Live Stream", frame)
            image_list.append(frame)
            
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            keepRecording = False
            
        time.sleep(1)
    cv2.destroyAllWindows()

recorder = Thread(target=video_stream)
recorder.start()

try:
    time.sleep(15)  
finally:
    keepRecording = False
    recorder.join()
    tello.streamoff()


 