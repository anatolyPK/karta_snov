import numpy as np
from dash import html

from src.common import Coordinates


def convert_geographical_to_rectangular_coords(point: Coordinates) -> tuple[float, float]:
    geogr_coords = np.array([
        [54.8256092814833, 18.012144932093065],
        [54.83120373592262, 18.24549937980945],
        [54.67262127727609, 18.00818827286221],
        [54.66902892641638, 18.24126977454898]
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
    x_rect, y_rect = map(
        lambda coord: f"{round(coord / 5) * 5:05}",
        convert_geographical_to_rectangular_coords(point)
    )
    return f'{x_rect[:2]} {x_rect[2:]}', f'{y_rect[:2]} {y_rect[2:]}'


def _get_meters_from_rectangular_coords(x: str, y: str) -> tuple[int, int]:
    return int(x[-3:]), int(y[-3:])


def _get_quadrant_from_rectangular_coords(x: str, y: str) -> tuple[str, str]:
    return x[:2], y[:2]


def convert_to_snail_4_coords(x_rect: str, y_rect: str) -> str:
    x_, y_ = _get_quadrant_from_rectangular_coords(x_rect, y_rect)
    x_meters, y_meters = _get_meters_from_rectangular_coords(x_rect, y_rect)
    if x_meters >= 500:
        if y_meters >= 500:
            return f'{x_}{y_}-Б'
        return f'{x_}{y_}-А'
    if y_meters <= 500:
        return f'{x_}{y_}-В'
    return f'{x_}{y_}-Г'


def convert_to_snail_9_coords(x_rect: str, y_rect: str) -> str:
    x_, y_ = _get_quadrant_from_rectangular_coords(x_rect, y_rect)
    x_meters, y_meters = _get_meters_from_rectangular_coords(x_rect, y_rect)
    if x_meters < 333:
        if y_meters < 333:
            return f'{x_}{y_}-7'
        elif y_meters < 666:
            return f'{x_}{y_}-6'
        return f'{x_}{y_}-5'

    if x_meters < 666:
        if y_meters < 333:
            return f'{x_}{y_}-8'
        elif y_meters < 666:
            return f'{x_}{y_}-9'
        return f'{x_}{y_}-4'

    if y_meters < 333:
        return f'{x_}{y_}-1'
    elif y_meters < 666:
        return f'{x_}{y_}-2'
    return f'{x_}{y_}-3'

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
            html.Div(html.Strong("Целеуказание по улитке (точность - 1/4 квадрата):"), className='mt-2'),
            html.Div(f'{convert_to_snail_4_coords(x_rect, y_rect)}'),
            html.Div(html.Strong("Целеуказание по улитке (точность - 1/9 квадрата):"), className='mt-2'),
            html.Div(f'{convert_to_snail_9_coords(x_rect, y_rect)}'),
        ]
    )