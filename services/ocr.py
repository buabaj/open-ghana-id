from __future__ import annotations

from typing import Optional

import pytesseract
from PIL import Image

from config import get_logger
from models import DriversLicenseData


def extract_ghana_card_number(image_path: str) -> Optional[str]:
    logger = get_logger()

    text = pytesseract.image_to_string(Image.open(image_path))
    try:
        candidates = [token for token in text.split() if token.startswith("GHA-")]
        return candidates[0]
    except IndexError:
        logger.error("Ghana card number not found in OCR text")
        return None


def serialize_drivers_license_data(text: str) -> Optional[DriversLicenseData]:
    logger = get_logger()

    try:
        lines = [line for line in text.split("\n") if line]
        names = lines[3].split(" ")
        first_name = names[0].capitalize()
        last_name = names[1].capitalize()
        other_names = " ".join(names[2:]).capitalize()
        dob = lines[5].split(" ")[0]
        nationality = lines[8].split(" ")[1].capitalize()
        issue_date = lines[8].split(" ")[0]
        expiry_date = lines[-1].split(" ")[2]
        license_number = lines[5].split(" ")[1]
        ref_number_parts = lines[-1].split(" ")[-2:]
        ref_number = "".join(ref_number_parts)
    except (IndexError, ValueError) as exc:
        logger.error(f"Drivers license data serialization failed: {exc}")
        return None

    return DriversLicenseData(
        first_name=first_name,
        last_name=last_name,
        other_names=other_names,
        date_of_birth=dob,
        nationality=nationality,
        issue_date=issue_date,
        expiry_date=expiry_date,
        license_number=license_number,
        ref_number=ref_number,
    )
