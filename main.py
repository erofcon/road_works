import os

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
import uvicorn
from loguru import logger

from app.models.database import database
from app.routes import user as users_routes
from app.routes import token as token_routes
from app.routes import task as tasks_routes
from app.routes import company as companies_routes
from app.routes import group as groups_routes
from app.routes import users_groups as users_groups_routes
from app.routes import answer as answers_routes
from app.routes import detection as detections_routes
from app.routes import detection_images as detection_images_routes
from app.routes import map as map_routes
from app.routes import car as car_routes

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")

app = FastAPI()

logger.add(f'/mnt/projects_files/road_works/logs/log.log', rotation="00:00")

add_pagination(app)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173", "http://0.0.0.0:8081", "http://192.168.0.10:8081",
                                  "http://192.168.2.33:5173",
                                  "http://192.168.0.10:8081",
                                  "http://192.168.2.36:8082",
                                  "http://0.0.0.0:5173",
                                  "http://localhost:8081",
                                  "http://192.168.10.218:8081",
                                  "http://127.0.0.1:43630",
                                  "http://192.168.10.144:8080",
                                  "http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")

app.include_router(router=users_routes.router)
app.include_router(router=token_routes.router)
app.include_router(router=tasks_routes.router)
app.include_router(router=companies_routes.router)
app.include_router(router=groups_routes.router)
app.include_router(router=users_groups_routes.router)
app.include_router(router=answers_routes.router)
app.include_router(router=detections_routes.router)
app.include_router(router=detection_images_routes.router)
app.include_router(router=map_routes.router)
app.include_router(router=car_routes.router)


@app.on_event('startup')
async def startup():
    logger.info('application launch')
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    logger.info('application stop')
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='0.0.0.0', port=8000
    )
