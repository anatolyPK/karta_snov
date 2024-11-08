from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_leaflet as dl

from src.text import dropdown_text

image_path = "assets/Snov_50000_page-0001.jpg"
image_bounds = [
    [54.6480, 17.99],
    [54.8458, 18.26]
]

control_section = html.Div(
    [
        dcc.Dropdown(
            [
                *dropdown_text.values()
            ],
            dropdown_text['coordinates'],
            clearable=False,
            id='dropdown',
            maxHeight=600,
            optionHeight=60
        ),
        dcc.Store(
            id='store',
            storage_type='memory',
            data={
                'output-distance-and-azimuth': [],
                'target': []
            }
        ),
        html.Div(id='output-coordinates', className='mt-2'),
        html.Div(id='output-distance-and-azimuth', className='mt-2'),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Номенклатура карты"),
                        dbc.Input(
                            placeholder="Введите номенклатуру",
                            type="text",
                            id='nomenclature_input'
                        )
                    ]
                ),
                html.Div(
                    id='nomenclature_table'
                )
            ],
            id='output-nomenclature',
            className='mt-2'
        ),
        html.Div(id='output-target-designation', className='mt-2')
    ],
    className='mt-3'
)

center = [
    (image_bounds[0][0] + image_bounds[1][0]) / 2 + 0.01,
    (image_bounds[0][1] + image_bounds[1][1]) / 2
]

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch(id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ],
    className='d-flex justify-content-end'
)

layout = html.Div(

    [
        html.Div(
            dl.Map(
                center=center,
                zoom=12,
                children=[
                    dl.ImageOverlay(url=image_path, bounds=image_bounds),
                ],
                style={'width': '100%', 'height': '93vh'},
                bounds=image_bounds,
                id='map'
            ),
            # width=12,
            # md=6,
            className='order-1 col-12 col-md-8'
        ),
        html.Div([
            color_mode_switch,
            control_section],
            # width=12,
            # md=4,
            className='order-2 col-6 col-md-4'
        )
    ],
    className="m-3 p-3 row"
)
