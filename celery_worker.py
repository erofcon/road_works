import time

from celery import Celery
from celery.utils.log import get_task_logger

celery = Celery('tasks', broker='redis://127.0.0.1:6379/0')
# 'redis://localhost:6379/0
celery_log = get_task_logger(__name__)


@celery.task
def create_order():
    # 5 seconds per 1 order
    complete_time_per_item = 5

    # Keep increasing depending on item quantity being ordered
    time.sleep(complete_time_per_item)
    print("yesss")
    # Display log
    celery_log.info(f"Order Complete!")
    # return {"message": f"Hi {name}, Your order has completed!",
    #         "order_quantity": quantity}

# @celery.task(bind=True)
# def run_detection(a: int):
#     time.sleep(10)
#     print("hello nigers")
#     celery_log.info("order completed")
