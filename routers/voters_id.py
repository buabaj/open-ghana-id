from __future__ import annotations

import tempfile
from pathlib import Path

import aiofiles
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from config import get_logger
from models import ApiResponse
from services.qr import extract_voters_qr_data

router = APIRouter(tags=["voters-id"])

ACCEPTABLE_EXTENSIONS = {"png", "jpg", "jpeg"}


@router.post("/validate-voters-id", response_model=ApiResponse, response_model_exclude_none=True)
async def validate_voters_id(file: UploadFile = File(...)) -> ApiResponse | JSONResponse:
    logger = get_logger()

    suffix = file.filename.split(".")[-1].lower()
    if suffix not in ACCEPTABLE_EXTENSIONS:
        return JSONResponse(
            status_code=400,
            content=ApiResponse(success=False, message="File type not supported. Accepted: png, jpg, jpeg").model_dump(exclude_none=True),
        )

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "image.png"
            async with aiofiles.open(tmp_path, "wb") as out:
                content = await file.read()
                await out.write(content)

            result = extract_voters_qr_data(str(tmp_path))

        if result is None:
            return JSONResponse(
                status_code=422,
                content=ApiResponse(success=False, message="Could not extract QR data from voters ID image").model_dump(exclude_none=True),
            )

        return ApiResponse(
            success=True,
            message="Voters ID data extracted successfully",
            data=result.model_dump(mode="json"),
        )
    except Exception as exc:
        logger.error(f"Error processing voters id image: {exc}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse(success=False, message="Internal error processing voters ID image").model_dump(exclude_none=True),
        )
