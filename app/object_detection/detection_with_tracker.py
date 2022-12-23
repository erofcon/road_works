import os
import time
from datetime import datetime

import cv2 as cv
from sqlalchemy.orm import Session
from app.models.database import database
from app.crud import tracker_data as tracker_data_crud
from app.crud import detections as detections_crud
from app.crud import detection_images as detection_images_crud
from app.schemas.detections import DetectionsCreate
from app.schemas.detection_images import DetectionImagesCreate
from app.object_detection.detection_stream import DetectionStream


async def run_detection(creator_id: int, video_path: str, video_start_datetime: datetime, description: str | None,
                        db: Session):
    # images: list[DetectionImagesCreate] = []
    # count_detect_img = 0
    # images_path = f'static/detection_files/detection_with_tracker/{datetime.now().strftime("%Y-%m-%d")}/detection_images'
    #
    # video_start_datetime = datetime.strptime(str(video_start_datetime), "%Y-%m-%dT%H:%M:%S")
    # detection_stream = DetectionStream(video_path=video_path,
    #                                    yolo_path='detection_files/yolov4-pothole.weights',
    #                                    cfg_path='detection_files/yolov4-pothole.cfg',
    #                                    video_start_time=video_start_datetime).start()
    #
    # if not os.path.isdir(images_path):
    #     os.makedirs(images_path)
    #
    # while not detection_stream.stopped or detection_stream.size() > 0:
    #
    #     if detection_stream.size() > 0:
    #         frame, current_time = detection_stream.read()
    #
    #         tracker_data = await tracker_data_crud.get_current_location(current_time)
    #
    #         image = f"{images_path}/{datetime.now().strftime('%Y-%m-%d-%H-%M')}_{count_detect_img}.jpg"
    #         cv.imwrite(image, frame)
    #
    #         image_model = DetectionImagesCreate(url=image, latitude=tracker_data.latitude,
    #                                             longitude=tracker_data.longitude)
    #         images.append(image_model)
    #
    #         count_detect_img += 1
    #
    #     else:
    #         time.sleep(0.1)
    #
    # cv.destroyAllWindows()
    # detection_stream.stop()

    detection_model = DetectionsCreate(description=description, creator_id=creator_id)

    detection_model_id = detections_crud.create_detection(detection=detection_model)
    #
    # if detection_model_id:
    #     for image in images:
    #         await detection_images_crud.create_detection_images(detection_images=image, detection_id=detection_model_id)
