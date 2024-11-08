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


def subtract_angle(initial_angle: float) -> str:
    total_degrees_to_subtract = SUBTRACT_ANGLE[0] + SUBTRACT_ANGLE[1] / 60

    resulting_angle = (initial_angle - total_degrees_to_subtract) % 360

    resulting_degrees = int(resulting_angle)
    resulting_minutes = int((resulting_angle - resulting_degrees) * 60)

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
    return subtract_angle(angle_between_points)

