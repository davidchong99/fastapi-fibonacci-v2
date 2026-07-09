import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.router import api_router
from app.core.config import SETTINGS
from app.services.fibonacci import generate_fibonacci


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Generate the Fibonacci series up to the max int possible with the underlying OS
    app.state.fibonacci = generate_fibonacci(sys.maxsize)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fibonacci API",
        version="1.0.0",
        root_path="/fibonacci/v1/",
        lifespan=lifespan,
    )
    app.include_router(api_router)
    add_pagination(app)
    return app


app = create_app()


def main() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=SETTINGS.server_port,
        log_level=SETTINGS.server_log_level,
    )


if __name__ == "__main__":
    main()
