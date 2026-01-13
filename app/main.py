import sys
import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi_pagination import Page, add_pagination, paginate
from app.env import SETTINGS


def fibonacci(nterm: int) -> list:
    a = 0
    b = 1
    result = [a]
    while b <= nterm:
        result.append(b)
        a, b = b, a + b

    return result


app = FastAPI(title="Fibonacci API", version="1.0.0")
add_pagination(app)

# Generate the Fibonacci series up the max int possible with underlying OS
app.state.fibonacci = fibonacci(sys.maxsize)


@app.get("/", response_class=PlainTextResponse)
async def get_root():
    return "Root ..."


@app.get("/all")
async def get_all() -> Page[int]:
    return paginate(app.state.fibonacci)


if __name__ == "__main__":
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=SETTINGS.server_port,
        log_level=SETTINGS.server_log_level,
    )
