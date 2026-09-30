from fastapi import FastAPI

from .database import Base, engine
from . import models

from .routers import incidents
from .routers import resources
from .routers import replanning


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Industrial Crisis Command AI",
    version="1.0.0",
    description="Multi-Agent Industrial Accident Crisis Command Backend"
)


app.include_router(incidents.router)
app.include_router(resources.router)
app.include_router(replanning.router)


@app.get("/")
def root():
    return {
        "message": "Industrial Crisis Command AI Backend is running"
    }