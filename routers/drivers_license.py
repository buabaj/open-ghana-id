from __future__ import annotations

import tempfile
from pathlib import Path

import aiofiles
import pytesseract
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from config import get_logger
from models import ApiResponse
from services.image_processing import process_image
from services.ocr import serialize_drivers_license_data

router = APIRouter(tags=["drivers-license"])

ACCEPTABLE_EXTENSIONS = {"png", "jpg", "jpeg"}


@router.post("/validate-drivers-license", response_model=ApiResponse, response_model_exclude_none=True)
async def validate_drivers_license(file: UploadFile = File(...)) -> ApiResponse | JSONResponse:
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

            processed = process_image(str(tmp_path))
            raw_text = pytesseract.image_to_string(processed)
            result = serialize_drivers_license_data(raw_text)

        if result is None:
            return JSONResponse(
                status_code=422,
                content=ApiResponse(success=False, message="Could not extract data from drivers license image").model_dump(exclude_none=True),
            )

        return ApiResponse(
            success=True,
            message="Drivers license data extracted successfully",
            data=result.model_dump(),
        )
    except Exception as exc:
        logger.error(f"Error processing drivers license image: {exc}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse(success=False, message="Internal error processing drivers license image").model_dump(exclude_none=True),
        )
