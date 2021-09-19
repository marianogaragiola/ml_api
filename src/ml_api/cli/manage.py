import uvicorn
import typer

from gunicorn.app.base import BaseApplication
from ml_api.settings import gunicorn_settings, settings


app = typer.Typer()


class StandaloneApplication(BaseApplication):
    """
    A simple implementation of a Gunicorn Application
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@app.command()
def start():
    """Start the API with Gunicorn"""
    StandaloneApplication(settings.APP_MODULE, gunicorn_settings.dict()).run()


@app.command()
def start_reload():
    typer.echo("Running API with reload mode")
    uvicorn.run(app="ml_api.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    app()
