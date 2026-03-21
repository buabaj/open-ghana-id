from __future__ import annotations

import tempfile
from pathlib import Path

import aiofiles
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from config import get_logger
from models import ApiResponse, MrzData
from services.mrz import detect_and_extract_mrz

router = APIRouter(tags=["ghana-card"])

ACCEPTABLE_EXTENSIONS = {"png", "jpg", "jpeg"}


@router.post("/validate-ghana-card", response_model=ApiResponse, response_model_exclude_none=True)
async def validate_ghana_card(file: UploadFile = File(...)) -> ApiResponse | JSONResponse:
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

            mrz_data = detect_and_extract_mrz(str(tmp_path))
            if mrz_data is None:
                return JSONResponse(
                    status_code=422,
                    content=ApiResponse(success=False, message="Could not extract MRZ data from Ghana card image").model_dump(exclude_none=True),
                )

        return ApiResponse(
            success=True,
            message="Ghana card MRZ data extracted successfully",
            data=MrzData(**mrz_data).model_dump(),
        )
    except Exception as exc:
        logger.error(f"Error processing ghana card image: {exc}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse(success=False, message="Internal error processing Ghana card image").model_dump(exclude_none=True),
        )
