import numpy as np
from dash import html

from src.common import Coordinates


def convert_geographical_to_rectangular_coords(point: Coordinates) -> tuple[float, float]:
    geogr_coords = np.array([
        [54.82464672815769, 18.011738149047737],
        [54.83130740228322, 18.244740079082476],
        [54.67264603461943, 18.007958634613473],
        [54.670179901790334, 18.241498226175356]
    ])

    react_coords = np.array([
        [82000, 8000],
        [82000, 23000],
        [65000, 7000],
        [64000, 22000]
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
    return x_rect, y_rect


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
            html.Div(f"Х=60{x_rect}"),
            html.Div(f"Y=43{y_rect}"),
            html.Div(html.Strong("Сокращенные прямоугольные координаты объекта:"), className='mt-2'),
            html.Div(f"Х={x_rect}"),
            html.Div(f"Y={y_rect}"),
        ]
    )