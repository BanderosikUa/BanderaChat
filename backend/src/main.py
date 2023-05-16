import json

import fastapi.openapi.utils as fu
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, ValidationError, HTTPException

from starlette.responses import JSONResponse

from src.config import app_configs, settings
from src.exceptions import CustomValidationError
from src.schemas import ErrorResponse

from src.auth.routers import router as auth_router
from src.chat.routers import router as chat_router

fu.validation_error_response_definition = ErrorResponse.schema()
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

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
@app.exception_handler(CustomValidationError)
async def validation_exception_handler(request, exc: RequestValidationError|CustomValidationError) -> ErrorResponse:
    exc_json = json.loads(exc.json())
    response = {"status": "error", "detail": []}
    for error in exc_json:
        response['detail'].append({error['loc'][-1]: error['msg']})

    return JSONResponse(response, status_code=422)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chat_router, tags=["Chat"])
