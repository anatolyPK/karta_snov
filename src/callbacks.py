from dataclasses import asdict

from dash import callback, Output, Input, html, State, no_update, clientside_callback

from src.common import Coordinates
from src.services.coord_converter import get_coordinates
from src.services.distance_and_angle import calculate_distance, calculate_azimuth
from src.services.nomenclature_finder import get_nomenclature_table
from src.exceptions import InvalidNomenclature
from src.services.target_destination import calculate_target_destination
from src.text import dropdown_text


@callback(
    Output('output-coordinates', 'style'),
    Output('output-distance-and-azimuth', 'style'),
    Output('output-nomenclature', 'style'),
    Output('output-target-designation', 'style'),
    Input('dropdown', 'value')
)
def update_main_block(value):
    if value == dropdown_text['coordinates']:
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    elif value == dropdown_text['dist_and_azimuth']:
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    elif value == dropdown_text['nomenclature']:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    elif value == dropdown_text['target']:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
    else:
        raise ValueError('Invalid dropdown value')


@callback(
    Output("output-distance-and-azimuth", "children"),
    Output('store', 'data', allow_duplicate=True),
    Input('map', 'n_clicks'),
    Input('dropdown', 'value'),
    State('map', 'clickData'),
    State('dropdown', 'value'),
    State('store', 'data'),
    prevent_initial_call=True
)
def find_distance_and_azimuth(n_click, dropdown_value_tmp, data, dropdown_value, storage):
    if dropdown_value == dropdown_text['dist_and_azimuth'] and n_click:
        point = Coordinates(latitude=data['latlng']['lat'], longitude=data['latlng']['lng'])

        if not storage['output-distance-and-azimuth']:
            point_dict = asdict(point)
            storage['output-distance-and-azimuth'].append(point_dict)
            return 'Кликните на второй объект', storage

        else:
            first_point_dict = storage['output-distance-and-azimuth'][0]
            dist = calculate_distance(Coordinates(**first_point_dict), point)
            angle = calculate_azimuth(Coordinates(**first_point_dict), point)
            storage['output-distance-and-azimuth'] = []
            return html.Div(
                [
                    html.Div(html.Strong("Расстояние:")),
                    html.Div(f"L={dist} метров"),
                    html.Div(html.Strong("Магнитный азимут"), className='mt-2'),
                    html.Div(f"Ам={angle}")
                ]
            ), storage

    return "Кликните на первый объект, а затем на второй", no_update

@callback(
    Output('output-coordinates', 'children'),
    Input('map', 'n_clicks'),
    State('map', 'clickData'),
    State('dropdown', 'value')
)
def display_coordinates(n_click, data, dropdown_value):
    if n_click is not None and dropdown_value == dropdown_text['coordinates']:
        point = Coordinates(latitude=data['latlng']['lat'], longitude=data['latlng']['lng'])
        return get_coordinates(point)
    return "Кликните на карту, чтобы получить координаты."


@callback(
    Output('nomenclature_table', 'children'),
    Input('nomenclature_input', 'value'),
    State('dropdown', 'value')
)
def calculate_nomenclature(value, dropdown_value):
    if value is not None and dropdown_value == dropdown_text['nomenclature']:
        try:
            table = get_nomenclature_table(value)
        except InvalidNomenclature:
            return html.Div('Проверьте введенную номенклатуру', className='mt-3')
        return table
    return "Введите номенклатуру"

@callback(
    Output("output-target-designation", "children"),
    Output('store', 'data'),
    Input('map', 'n_clicks'),
    State('map', 'clickData'),
    State('dropdown', 'value'),
    State('store', 'data')
)
def get_target_destination(n_click, data, dropdown_value, storage):
    if dropdown_value == dropdown_text['target'] and n_click:
        point = Coordinates(latitude=data['latlng']['lat'], longitude=data['latlng']['lng'])

        if not storage['target']:
            point_dict = asdict(point)
            storage['target'].append(point_dict)
            return 'Кликните на конец условной линии', storage
        elif len(storage['target']) == 1:
            point_dict = asdict(point)
            storage['target'].append(point_dict)
            return 'Кликните на цель', storage
        else:
            first_point_dict, second_point_dict = storage['target'][0], storage['target'][1]
            target_destination = calculate_target_destination(
                Coordinates(**first_point_dict),
                Coordinates(**second_point_dict),
                point)
            storage['target'] = []
            return target_destination, storage

    return "Кликните на начало условной линии", no_update


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark"); 
       return window.dash_clientside.no_update;
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)