import uvicorn
import typer


app = typer.Typer()

@app.command()
def start():
    typer.echo('Not supported yet')


@app.command()
def start_reload():
    typer.echo('Running API with reload mode')
    uvicorn.run(
        app='ml_api.app:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )


if __name__ == '__main__':
    app()
