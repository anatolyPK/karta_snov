import math

from src.common import Coordinates, EARTH_RADIUS, SUBTRACT_ANGLE


def calculate_distance(first_point: Coordinates, second_point: Coordinates) -> int:
    phi1 = math.radians(first_point.latitude)
    phi2 = math.radians(second_point.latitude)
    delta_phi = math.radians(second_point.latitude - first_point.latitude)
    delta_lambda = math.radians(second_point.longitude - first_point.longitude)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS * c
    return round(distance / 5) * 5


def subtract_angle(initial_angle: float) -> float:
    total_degrees_to_subtract = SUBTRACT_ANGLE[0] + SUBTRACT_ANGLE[1] / 60
    return (initial_angle - total_degrees_to_subtract) % 360

def extract_degrees_and_minutes(angle: float) -> tuple[int, int]:
    resulting_degrees = int(angle)
    remaining_angle = angle - resulting_degrees

    resulting_minutes = int(abs(remaining_angle) * 60)
    resulting_seconds = int((abs(remaining_angle) * 3600) % 60)
    if resulting_seconds >= 30:
        resulting_minutes += 1

    if resulting_minutes >= 60:
        resulting_degrees += 1
        resulting_minutes = 0
    return resulting_degrees, resulting_minutes

def format_angle_in_str_format(angle: float) -> str:
    resulting_degrees, resulting_minutes = extract_degrees_and_minutes(angle)
    return f"{resulting_degrees}° {resulting_minutes}'"

def calculate_angle_between_points(first_point: Coordinates, second_point: Coordinates) -> float:
    lat1, lon1 = map(math.radians, (first_point.latitude, first_point.longitude))
    lat2, lon2 = map(math.radians, (second_point.latitude, second_point.longitude))
    delta_lon = lon2 - lon1

    angle = math.atan2(
        math.sin(delta_lon) * math.cos(lat2),
        math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    )

    angle_degrees = (math.degrees(angle) + 360 + 2.4) % 360
    return angle_degrees

def calculate_azimuth(first_point: Coordinates, second_point: Coordinates) -> str:
    angle_between_points = calculate_angle_between_points(first_point, second_point)
    resulting_angle = subtract_angle(angle_between_points)
    return format_angle_in_str_format(resulting_angle)

