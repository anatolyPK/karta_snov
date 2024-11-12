import dash_bootstrap_components as dbc
from dash import html

from src.common import Coordinates
from src.services.distance_and_angle import calculate_azimuth, calculate_distance


def get_road_scheme_table(first_point: Coordinates, second_point: Coordinates, third_point: Coordinates) -> dbc.Table:
    point_pairs = [
        (first_point, second_point),
        (second_point, third_point),
        (third_point, first_point)
    ]
    point_names = ('A - B', 'B - C', 'C - A')

    distances_and_azimuths = [
        (calculate_distance(point1, point2), calculate_azimuth(point1, point2)) for point1, point2 in point_pairs
    ]

    table_rows = []
    for road_name, (distance, azimuth) in zip(point_names, distances_and_azimuths):
        table_rows.append(html.Tr([
            html.Td(road_name),
            html.Td(f"{distance}"),
            html.Td(f"{azimuth}")
        ]))

    table_header = html.Thead(html.Tr([
        html.Th("Пара точек"),
        html.Th("Расстояние"),
        html.Th("Азимут")
    ]))

    return dbc.Table([table_header, html.Tbody(table_rows)], bordered=True, className='mt-3')