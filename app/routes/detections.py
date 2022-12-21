from fastapi import APIRouter, HTTPException, Depends, status

from celery_worker import create_order

router = APIRouter()


@router.post('/run_detection')
async def detection():
    # create_order.delay("temirlan", 1)
    create_order.delay()
    # run_detection.delay(1)
    return HTTPException(status_code=status.HTTP_200_OK)
