from __future__ import annotations

from datetime import datetime
from typing import Optional

import cv2

from config import get_logger
from models import VotersIdData


def extract_voters_qr_data(image_path: str) -> Optional[VotersIdData]:
    logger = get_logger()

    image = cv2.imread(image_path)
    if image is None:
        logger.error("Could not read image for QR extraction")
        return None

    detector = cv2.QRCodeDetector()
    data, vertices_array, _ = detector.detectAndDecode(image)

    if vertices_array is None or not data:
        return None

    try:
        parts = [s.capitalize() for s in data.split(">") if s]
        last_name = parts[0]
        first_name = parts[1]
        gender = parts[2]
        dob_raw = parts[3]
        polling_station = parts[4]
        reg_date_raw = parts[5]
        id_number = parts[6]

        dob = datetime.strptime(dob_raw, "%Y%m%d").date()
        registration_date = datetime.strptime(reg_date_raw, "%Y%m%d").date()

        return VotersIdData(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            id_number=id_number,
            date_of_birth=dob,
            registration_date=registration_date,
            polling_station_code=polling_station,
        )
    except (IndexError, ValueError) as exc:
        logger.error(f"QR code data extraction failed: {exc}")
        return None
