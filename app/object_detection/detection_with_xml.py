import os
import time
from datetime import datetime

import cv2 as cv
from sqlalchemy.orm import Session
from app.crud import detection as detections_crud
from app.crud import detection_images as detection_images_crud
from app.crud import detection_locations as detection_locations_crud
from app.schemas.detection import DetectionCreate
from app.schemas.detection_images import DetectionImagesCreate
from app.object_detection.detection_stream import DetectionStream
from app.object_detection.xmlparse import XmlPars


def run_detection(creator_id: int, video_path: str, xml_path: str, description: str | None, db: Session):
    images: list[DetectionImagesCreate] = []
    count_detect_img = 0
    images_path = f'static/detection_files/detection_with_xml/{datetime.now().strftime("%Y-%m-%d")}/detection_images'

    xml = XmlPars(xml_path=xml_path)

    detection_stream = DetectionStream(video_path=video_path,
                                       yolo_path='detection_files/yolov4-pothole.weights',
                                       cfg_path='detection_files/yolov4-pothole.cfg',
                                       video_start_time=xml.get_start_datetime()).start()

    if not os.path.isdir(images_path):
        os.makedirs(images_path)

    while not detection_stream.stopped or detection_stream.size() > 0:

        if detection_stream.size() > 0:
            frame, current_time = detection_stream.read()

            location = xml.get_current_location(current_time)
            image = f"{images_path}/{datetime.now().strftime('%Y-%m-%d-%H-%M')}_{count_detect_img}.jpg"
            cv.imwrite(image, frame)

            image_model = DetectionImagesCreate(url=image, latitude=location.latitude, longitude=location.longitude)
            images.append(image_model)

            count_detect_img += 1
        else:
            time.sleep(0.1)

    cv.destroyAllWindows()
    detection_stream.stop()

    detection_model = DetectionCreate(description=description, creator_id=creator_id)

    detection_model_id = detections_crud.create_detection(detection=detection_model, db=db)

    if detection_model_id:
        for image in images:
            detection_images_crud.create_detection_images(detection_images=image, detection_id=detection_model_id,
                                                          db=db)

    locations = xml.get_all_location()

    for location in locations:
        detection_locations_crud.create_detection(detection_locations=location, detection_id=detection_model_id, db=db)
