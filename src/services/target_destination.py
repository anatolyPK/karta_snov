from math import sqrt, radians, cos, sin

from src.common import digits, SM_IN_ONE_METER, Coordinates, Direction
from src.services.distance_and_angle import calculate_distance, EARTH_RADIUS


def get_string_distance(distance: float) -> str:
    first_digit, second_digit = str(round(distance * SM_IN_ONE_METER, 1)).split('.')
    try:
        return f'{digits[first_digit]} и {digits[second_digit]}'
    except KeyError:
        return f'{first_digit} и {second_digit}'


def calculate_side_of_line(first_point: Coordinates, second_point: Coordinates, third_point: Coordinates) -> Direction:
    det = ((second_point.latitude - first_point.latitude) * (third_point.longitude - first_point.longitude)
           - (second_point.longitude - first_point.longitude) * (third_point.latitude - first_point.latitude))
    return Direction.right if det > 0 else Direction.left


def to_cartesian(latitude: Coordinates.latitude, longitude: Coordinates.longitude) -> tuple[float, float, float]:
    """Переводит географические координаты (широту, долготу) в 3D-картезианские координаты."""
    lat_rad = radians(latitude)
    lon_rad = radians(longitude)
    return (
        EARTH_RADIUS * cos(lat_rad) * cos(lon_rad),
        EARTH_RADIUS * cos(lat_rad) * sin(lon_rad),
        EARTH_RADIUS * sin(lat_rad)
    )


def perpendicular_distance_geographic(
        first_point: Coordinates,
        second_point: Coordinates,
        third_point: Coordinates
) -> float:
    """Находит перпендикулярное расстояние от точки C до линии AB в географических координатах."""
    # Преобразуем точки в картезианские координаты
    ax, ay, az = to_cartesian(first_point.latitude, first_point.longitude)
    bx, by, bz = to_cartesian(second_point.latitude, second_point.longitude)
    cx, cy, cz = to_cartesian(third_point.latitude, third_point.longitude)
    cross_length = sqrt(
        ((by - ay) * (cz - az) - (bz - az) * (cy - ay)) ** 2 +
        ((bz - az) * (cx - ax) - (bx - ax) * (cz - az)) ** 2 +
        ((bx - ax) * (cy - ay) - (by - ay) * (cx - ax)) ** 2
    )
    ab_length = sqrt((bx - ax) ** 2 + (by - ay) ** 2 + (bz - az) ** 2)
    return cross_length / ab_length


def calculate_target_destination(
        first_point: Coordinates,
        second_point: Coordinates,
        third_point: Coordinates
) -> str:
    dist = get_string_distance(calculate_distance(first_point, second_point))
    side = calculate_side_of_line(first_point, second_point, third_point)
    perpendicular_distance = get_string_distance(
        perpendicular_distance_geographic(first_point, second_point, third_point)
    )
    return f'Прямая АВ {dist}, {side.value} {perpendicular_distance}, !НАИМЕНОВАНИЕ ОБЪЕКТА!'
