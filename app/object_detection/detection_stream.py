from __future__ import annotations

from datetime import datetime, timedelta
import time
from queue import Queue
from threading import Thread

import cv2 as cv
import numpy as np

from .sort import Sort


class DetectionStream:

    def __init__(self, video_path: str, yolo_path: str, cfg_path: str,
                 confidence_threshold: float = 0.5, nms_threshold: float = 0.4,
                 video_start_time: datetime = datetime.now(),
                 queue_size: int = 100):

        self.capture = cv.VideoCapture(video_path)

        self.video_start_time = video_start_time
        self.current_time = datetime.now()

        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold

        self.net = cv.dnn.readNet(yolo_path, cfg_path)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

        self.model = cv.dnn_DetectionModel(self.net)

        self.model.setInputParams(size=(480, 480), scale=1 / 255, swapRB=True)
        self.sort = Sort(max_age=30, min_hits=3, iou_threshold=0.1)

        self.trackerIds = np.zeros(0)
        self.frameCount = 0

        self.Q = Queue(maxsize=queue_size)

        self.thread = Thread(target=self.__update, args=())
        self.thread.daemon = True

        self.stopped = False

    def start(self) -> DetectionStream:
        self.thread.start()
        return self

    def read(self) -> tuple:
        return self.Q.get()

    def size(self) -> int:
        return self.Q.qsize()

    def stop(self) -> None:
        self.stopped = True
        self.thread.join()

    @staticmethod
    def get_time(milliseconds):
        seconds_t = milliseconds // 1000
        minutes_t = 0
        hours_t = 0

        if seconds_t >= 60:
            minutes_t = seconds_t // 60
            seconds_t = seconds_t % 60

        if minutes_t >= 60:
            hours_t = minutes_t // 60
            minutes_t = minutes_t % 60

        return hours_t, minutes_t, seconds_t

    def __update(self) -> None:
        while True:

            if self.stopped:
                break

            if not self.Q.full():

                (grabbed, frame) = self.capture.read()

                if not grabbed:
                    self.stopped = True
                    break

                milliseconds = self.capture.get(cv.CAP_PROP_POS_MSEC)

                if milliseconds > 0:
                    hours, minutes, seconds = self.get_time(milliseconds=milliseconds)
                    self.current_time = self.video_start_time + timedelta(hours=hours, minutes=minutes, seconds=seconds)

                    classes, scores, boxes = self.model.detect(frame, self.confidence_threshold, self.nms_threshold)

                    if len(scores) > 0:
                        self.__tracking(frame=frame, scores=scores, boxes=boxes)

                    if self.frameCount != 0:
                        self.frameCount -= 1

                    #cv.imshow("frame", frame)
                    if cv.waitKey(1) == ord('q'):
                        break

            else:
                time.sleep(0.1)

        cv.destroyAllWindows()
        self.capture.release()

    def __tracking(self, frame, scores, boxes) -> None:
        detect = np.array(
            [[box[0], box[1], (box[0] + box[2]), (box[1] + box[3]), score] for (score, box) in
             zip(scores, boxes)])

        tracker = self.sort.update(detect)

        if len(tracker) > 0:
            evaluate_any = np.isin(tracker[:, 4], self.trackerIds).any()
            evaluate_all = np.isin(tracker[:, 4], self.trackerIds).all()

            for d in tracker:
                cv.rectangle(frame, (int(d[0]), int(d[1])), (int(d[2]), int(d[3])),
                             (245, 23, 12), 2)
                # cv.putText(frame, str(d[4]), (int(d[0]), int(d[3])), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            if not evaluate_all:
                self.trackerIds = np.append(self.trackerIds, tracker[:, 4])

            if not evaluate_any and self.frameCount == 0:
                self.frameCount = 60
                self.Q.put((frame, self.current_time))
