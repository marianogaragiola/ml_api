"""
This file contains the main app, and some configs.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ml_api.api.validators import ApiVersionModel
from ml_api.api.routers import sentiment_analysis
from ml_api.api.handlers import start_app_handler, stop_app_handler
from ml_api.settings import API_VERSION


__version__ = API_VERSION

app = FastAPI(
    title='Machine Learning API',
    description='Machine Learning API',
    version=API_VERSION,
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/version", tags=["version"], response_model=ApiVersionModel)
def get_api_version():
    """ Get API information. """

    return ApiVersionModel(
        title=app.title, description=app.description, version=app.version
    )


app.include_router(
    sentiment_analysis.router,
    prefix='/sentiment',
    tags=['sentiment']
)

app.add_event_handler(
    "startup",
    start_app_handler(app)
)
app.add_event_handler(
    "shutdown",
    stop_app_handler(app)
)
