import time

import cv2 as cv

from app.object_detection.detection_stream import DetectionStream
from app.object_detection.xmlparse import XmlPars

xml = XmlPars(xml_path='detection_files/2022-11-30T10_11_08.310580.xml')

detection = DetectionStream(video_path='detection_files/test_video.mp4',
                            yolo_path='detection_files/yolov4-pothole.weights',
                            cfg_path='detection_files/yolov4-pothole.cfg',
                            video_start_time=xml.get_start_datetime()).start()
i = 0

while not detection.stopped or detection.size() > 0:

    if detection.size() > 0:
        (frame, current_time) = detection.read()
        location = xml.get_current_location(current_time)
        print(location.latitude, " ", location.longitude)
        filename = f'savedImage_{i}.jpg'
        cv.imwrite(filename, frame)
        i += 1

    else:
        time.sleep(0.1)

cv.destroyAllWindows()
detection.stop()
