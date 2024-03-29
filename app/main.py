from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings

from fastapi import APIRouter
from app.api.v1 import projects
from app.api.v1 import about
from app.api import home

from . import models, schemas
from .database import SessionLocal, engine


def get_application():
    models.Base.metadata.create_all(bind=engine)
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app



api_router = APIRouter()
api_router.include_router(projects.router, prefix="/api/v1", tags=["projects"])
api_router.include_router(about.router, prefix="/api/v1", tags=["about"])

api_router.include_router(home.router, tags=["home", "index"])

app = get_application()
app.include_router(api_router)
app.mount("/", StaticFiles(directory="/home/jflorchi/dev/jflorchi.ca/app/static", html=True), name="static")
