from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings
from models import ApiResponse
from routers import (
    drivers_license,
    ghana_card,
    ghana_card_number,
    passport,
    tin,
    voters_id,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Pydantic/FastAPI request validation errors → 400 with ApiResponse envelope."""
    return JSONResponse(
        status_code=400,
        content=ApiResponse(success=False, message=str(exc.errors()[0]["msg"])).model_dump(exclude_none=True),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected errors → 500 with ApiResponse envelope."""
    return JSONResponse(
        status_code=500,
        content=ApiResponse(success=False, message="Internal server error").model_dump(exclude_none=True),
    )


@app.get("/", response_model=ApiResponse, response_model_exclude_none=True)
async def root() -> ApiResponse:
    return ApiResponse(
        success=True,
        message="Welcome to the Open Ghana ID pre-verification API",
    )


@app.get("/health", response_model=ApiResponse, response_model_exclude_none=True)
async def health() -> ApiResponse:
    return ApiResponse(success=True, message="Service is healthy")


app.include_router(passport.router)
app.include_router(ghana_card.router)
app.include_router(voters_id.router)
app.include_router(drivers_license.router)
app.include_router(tin.router)
app.include_router(ghana_card_number.router)
