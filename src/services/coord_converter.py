import numpy as np
from dash import html

from src.common import Coordinates


def convert_geographical_to_rectangular_coords(point: Coordinates) -> tuple[float, float]:
    geogr_coords = np.array([
        [54.825601760380074, 18.012151993947885],
        [54.83120848463973, 18.245496406522513],
        [54.672672628913601656656112767, 18.00817180059734],
        [54.669034014908995, 18.24126505550682]
    ])

    react_coords = np.array([
        [82020, 8020],
        [81990, 22985],
        [65000, 6985],
        [64000, 22015]
    ])
    matrix = np.linalg.lstsq(
        np.vstack([geogr_coords.T, np.ones(4)]).T,
        react_coords,
        rcond=None
    )[0]

    real_point = np.dot(np.array([point.latitude, point.longitude, 1]), matrix)
    return real_point[0], real_point[1]


def decimal_to_dms(decimal: float) -> tuple[int, int, int]:
    degrees = int(decimal)
    minutes = int((decimal - degrees) * 60)
    seconds = int(((decimal - degrees) * 60 - minutes) * 60)
    return degrees, minutes, seconds


def convert_to_rectangular_coords(point: Coordinates) -> tuple[str, str]:
    x_rect, y_rect = map(lambda coord: f"{round(coord / 5) * 5:05}",
                         convert_geographical_to_rectangular_coords(point))
    return f'{x_rect[:2]} {x_rect[2:]}', f'{y_rect[:2]} {y_rect[2:]}'


def get_coordinates(point: Coordinates) -> html.Div:
    lat_deg, lat_min, lat_sec = decimal_to_dms(point.latitude)
    lon_deg, lon_min, lon_sec = decimal_to_dms(point.longitude)

    lat_str = f"{lat_deg}° {int(lat_min):02}' {int(lat_sec):02}\""
    lon_str = f"{lon_deg}° {int(lon_min):02}' {int(lon_sec):02}\""

    x_rect, y_rect = convert_to_rectangular_coords(point)

    return html.Div(
        [
            html.Div(html.Strong("Географические координаты объекта:")),
            html.Div(f"B={lat_str}"),
            html.Div(f"L={lon_str}"),
            html.Div(html.Strong("Полные прямоугольные координаты объекта:"), className='mt-2'),
            html.Div(f"Х=6 0{x_rect}"),
            html.Div(f"Y=4 3{y_rect}"),
            html.Div(html.Strong("Сокращенные прямоугольные координаты объекта:"), className='mt-2'),
            html.Div(f"Х={x_rect}"),
            html.Div(f"Y={y_rect}"),
        ]
    )