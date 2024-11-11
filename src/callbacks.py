from dataclasses import asdict

from dash import callback, Output, Input, html, State, clientside_callback
from dash.exceptions import PreventUpdate

from src.common import Coordinates
from src.services.azimuth import get_azimuth
from src.services.coord_converter import get_coordinates
from src.services.distance_and_angle import calculate_distance, calculate_azimuth
from src.services.nomenclature_finder import get_nomenclature_table
from src.exceptions import InvalidNomenclature, InvalidAngleFormat
from src.services.target_destination import calculate_target_destination
from src.text import dropdown_text


@callback(
    Output('output-coordinates', 'style'),
    Output('output-distance-and-azimuth', 'style'),
    Output('output-nomenclature', 'style'),
    Output('output-target-designation', 'style'),
    Output('output-azimuth', 'style'),
    Output('road-scheme', 'style'),
    Input('dropdown', 'value')
)
def update_main_block(value):
    index_map = {
        dropdown_text['coordinates']: 0,
        dropdown_text['dist_and_azimuth']: 1,
        dropdown_text['nomenclature']: 2,
        dropdown_text['target']: 3,
        dropdown_text['azimuth']: 4,
        dropdown_text['road_scheme']: 5
    }
    styles = [{'display': 'none'}] * len(index_map)

    if value in index_map:
        styles[index_map[value]] = {'display': 'block'}
    else:
        raise ValueError('Invalid dropdown value')

    return styles

@callback(
    Output("output-distance-and-azimuth", "children"),
    Output('store', 'data', allow_duplicate=True),
    Input('map', 'n_clicks'),
    State('map', 'clickData'),
    State('dropdown', 'value'),
    State('store', 'data'),
    prevent_initial_call=True
)
def find_distance_and_azimuth(n_click, data, dropdown_value, storage):
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

    raise PreventUpdate

@callback(
    Output('output-coordinates', 'children'),
    Input('map', 'n_clicks'),
    State('map', 'clickData'),
    State('dropdown', 'value'),
    prevent_initial_call=True
)
def display_coordinates(n_click, data, dropdown_value):
    if n_click is not None and dropdown_value == dropdown_text['coordinates']:
        point = Coordinates(latitude=data['latlng']['lat'], longitude=data['latlng']['lng'])
        return get_coordinates(point)
    raise PreventUpdate


@callback(
    Output('nomenclature_table', 'children'),
    Input('nomenclature_input', 'value'),
    State('dropdown', 'value'),
    prevent_initial_call=True
)
def calculate_nomenclature(value, dropdown_value):
    if value is not None and dropdown_value == dropdown_text['nomenclature']:
        try:
            table = get_nomenclature_table(value)
        except InvalidNomenclature:
            return html.Div('Проверьте введенную номенклатуру', className='mt-3')
        return table
    raise PreventUpdate


@callback(
    Output('azimuth-answer', 'children'),
    Input('azimuth_input', 'value'),
    State('dropdown', 'value'),
    prevent_initial_call=True
)
def calculate_from_directional_angle(value, dropdown_value):
    if value is not None and dropdown_value == dropdown_text['azimuth']:
        try:
            table = get_azimuth(value)
        except InvalidAngleFormat:
            return html.Div(
                'Проверьте введенный дирекционный угол. Поддерживаемые форматы: '
                'GG, GG.MM, где GG - градусы, MM - минуты',
                className='mt-3'
            )
        return table
    raise PreventUpdate


@callback(
    Output("output-target-designation", "children"),
    Output('store', 'data'),
    Input('map', 'n_clicks'),
    State('map', 'clickData'),
    State('dropdown', 'value'),
    State('store', 'data'),
    prevent_initial_call=True
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
                point
            )
            storage['target'] = []
            return target_destination, storage
    raise PreventUpdate


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