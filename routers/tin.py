from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from config import get_logger
from models import ApiResponse, TinRequest
from services.gra_client import GraUpstreamError, validate_tin

router = APIRouter(tags=["tin"])


@router.post("/validate-tin", response_model=ApiResponse, response_model_exclude_none=True)
async def verify_tin(payload: TinRequest) -> ApiResponse | JSONResponse:
    if not payload.tin_num:
        return JSONResponse(
            status_code=400,
            content=ApiResponse(success=False, message="Please enter a valid TIN.").model_dump(exclude_none=True),
        )

    logger = get_logger()
    logger.info("Validating TIN via GRA endpoint")

    try:
        is_valid = await validate_tin(payload.tin_num)
    except GraUpstreamError as exc:
        logger.error(f"GRA upstream error: {exc}")
        return JSONResponse(
            status_code=502,
            content=ApiResponse(success=False, message="GRA verification service is unavailable").model_dump(exclude_none=True),
        )

    if is_valid:
        return ApiResponse(success=True, message="Personal TIN is valid")
    return ApiResponse(success=False, message="Personal TIN is invalid")
