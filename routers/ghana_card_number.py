from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from config import get_logger
from models import ApiResponse, GhanaCardNumberRequest
from services.gra_client import GraUpstreamError, validate_ghana_card_number

router = APIRouter(tags=["ghana-card-number"])


@router.post("/validate-ghana-card-number", response_model=ApiResponse, response_model_exclude_none=True)
async def validate_ghana_card_number_route(
    payload: GhanaCardNumberRequest,
) -> ApiResponse | JSONResponse:
    if not payload.card_num:
        return JSONResponse(
            status_code=400,
            content=ApiResponse(success=False, message="Please enter a valid Ghana Card Number.").model_dump(exclude_none=True),
        )

    logger = get_logger()
    logger.info("Validating Ghana card number via GRA endpoint")

    try:
        is_valid = await validate_ghana_card_number(payload.card_num)
    except GraUpstreamError as exc:
        logger.error(f"GRA upstream error: {exc}")
        return JSONResponse(
            status_code=502,
            content=ApiResponse(success=False, message="GRA verification service is unavailable").model_dump(exclude_none=True),
        )

    if is_valid:
        return ApiResponse(success=True, message="Ghana card number is valid")
    return ApiResponse(success=False, message="Ghana card number is invalid")
