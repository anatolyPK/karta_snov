from src.common import SUBTRACT_ANGLE
from src.exceptions import InvalidAngleFormat
from src.services.distance_and_angle import subtract_angle, extract_degrees_and_minutes


def parse_directional_angle(directional_angle: str) -> float:
    directional_angle = directional_angle.strip()
    parts = directional_angle.split('.')

    if len(parts) < 1 or len(parts) > 2:
        raise InvalidAngleFormat

    try:
        degrees = int(parts[0])
        if degrees < 0 or degrees > 180:
            raise InvalidAngleFormat

        if len(parts) > 1:
            minutes = int(parts[1].ljust(2, '0'))
        else:
            minutes = 0

        if minutes < 0 or minutes >= 60:
            raise ValueError("Minutes must be between 0 and 59.")
    except ValueError as e:
        raise InvalidAngleFormat

    return degrees + (minutes / 60)


def get_azimuth(directional_angle: str) -> str:
    initial_angle = parse_directional_angle(directional_angle)
    angle = subtract_angle(initial_angle)
    initial_degrees, initial_minutes = extract_degrees_and_minutes(initial_angle)
    degrees, minutes = extract_degrees_and_minutes(angle)
    return f"{initial_degrees}° {initial_minutes}' - {SUBTRACT_ANGLE[0]}° {SUBTRACT_ANGLE[1]}' = {degrees}° {minutes}'"
