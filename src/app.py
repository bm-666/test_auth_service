import uvicorn
from fastapi import FastAPI

from api.router import routers
from config.settings import settings
from custom_exceptions.exception_handler import init_exception_handlers

app = FastAPI(root_path="/api/v1")
init_exception_handlers(app)
for router in routers:
    app.include_router(router)


def main():
    uvicorn.run(app, port=settings.FAST_API_PORT, host=settings.FAST_API_HOST)
