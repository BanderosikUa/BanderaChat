from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import app_configs, settings
from src.database import SessionLocal
from src.auth.routers import router as auth_router

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=settings.CORS_HEADERS,
)

@app.get("/")
def home():
    return "Hello, Worldfasdsadff!"


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
