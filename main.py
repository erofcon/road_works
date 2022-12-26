from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.models.database import database
from app.routes import users as users_routes
from app.routes import token as token_routes
from app.routes import tasks as tasks_routes
from app.routes import companies as companies_routes
from app.routes import groups as groups_routes
from app.routes import companies_groups as companies_groups_routes
from app.routes import users_groups as users_groups_routes
from app.routes import answers as answers_routes
from app.routes import detections as detections_routes

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:8081", "http://0.0.0.0:8081", "http://192.168.2.33:8081",
                                  " http://localhost:8081"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router=users_routes.router)
app.include_router(router=token_routes.router)
app.include_router(router=tasks_routes.router)
app.include_router(router=companies_routes.router)
app.include_router(router=groups_routes.router)
app.include_router(router=companies_groups_routes.router)
app.include_router(router=users_groups_routes.router)
app.include_router(router=answers_routes.router)
app.include_router(router=detections_routes.router)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
