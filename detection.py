import time

from app.object_detection.detection_stream import DetectionStream
from app.object_detection.xmlparse import XmlPars

xml = XmlPars(xml_path='detection_files/2022-11-30T10_11_08.310580.xml')

video_stream = DetectionStream(video_path='detection_files/test_video.mp4',
                               yolo_path='detection_files/yolov4-pothole.weights',
                               cfg_path='detection_files/yolov4-pothole.cfg',
                               video_start_time=xml.get_start_datetime()
                               ).start()

# while not video_stream.stopped:
#
#     if video_stream.size() > 0:
#         frame, current_time = video_stream.read()
#         print(current_time)
#
#     else:
#         time.sleep(1)
#
# video_stream.stop()
