import time
from datetime import datetime
import asyncio

from celery import Celery
from celery.utils.log import get_task_logger

from app.object_detection import detection_with_xml
from app.object_detection import detection_with_tracker

celery = Celery('tasks', broker='redis://127.0.0.1:6379/0')
celery_log = get_task_logger(__name__)


@celery.task
def run_detection_with_xml(creator_id: int, video_path: str, xml_path: str, description: str | None, ):
    asyncio.run(
        detection_with_xml.run_detection(creator_id=creator_id, video_path=video_path, xml_path=xml_path,
                                         description=description))


@celery.task
def run_detection_with_tracker(creator_id: int, video_path: str, video_start_datetime: datetime,
                               description: str | None):

    asyncio.run(
        detection_with_tracker.run_detection(creator_id=creator_id, video_path=video_path,
                                             video_start_datetime=video_start_datetime,
                                             description=description))
