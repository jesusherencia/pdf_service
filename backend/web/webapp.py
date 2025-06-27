from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from shared.logger import Logger
from web.rest_api_routes import router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == '__main__':
    Logger.set_current_logger_by_name("WEBAPP")
    uvicorn.run(app, port=8000, host='0.0.0.0')
