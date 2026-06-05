from fastapi import FastAPI
from .api.backend_api import router as backend_router
from .config.back_config import Settings

app = FastAPI()
app.include_router(backend_router)

if __name__ == "__main__":
    import uvicorn
    settings = Settings()
    uvicorn.run(app="src.backend.main:app", host=settings.API_HOST, port=settings.API_PORT)
