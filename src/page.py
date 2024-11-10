from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_leaflet as dl

from src.text import dropdown_text


image_path = "assets/Snov_50000.jpg"
image_bounds = [
    [54.6480, 17.99],
    [54.8458, 18.26]
]

control_section = html.Div(
    [
        dcc.Dropdown(
            [*dropdown_text.values()],
            dropdown_text['coordinates'],
            style={'color': 'black'},
            clearable=False,
            id='dropdown'
        ),
        dcc.Store(
            id='store',
            storage_type='memory',
            data={
                'output-distance-and-azimuth': [],
                'target': []
            }
        ),
        html.Div(
            "Кликните на карту, чтобы получить координаты.",
            id='output-coordinates',
            className='custom-margin-top'
        ),
        html.Div(
            "Кликните на первый объект, а затем на второй",
            id='output-distance-and-azimuth',
            className='custom-margin-top'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Номенклатура карты"),
                        dbc.Input(
                            placeholder="Введите номенклатуру",
                            type="text",
                            id='nomenclature_input',
                            className='text-size'
                        )
                    ]
                ),
                html.Div(
                    id='nomenclature_table'
                )
            ],
            id='output-nomenclature',
            className='custom-margin-top'
        ),
        html.Div(
            "Кликните на начало условной линии",
            id='output-target-designation',
            className='custom-margin-top fw-bold'
        )
    ]
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
    className='d-flex justify-content-end custom-margin'
)

layout = html.Div(
    [
        html.H1(
            'Учебная топографическая карта СНОВ У-34-37-В',
            className='d-flex justify-content-center text-center h1-size'
        ),
        html.Div(
            dl.Map(
                center=center,
                zoom=12,
                children=[
                    dl.ImageOverlay(url=image_path, bounds=image_bounds),
                ],
                style={'width': '100%'},
                bounds=image_bounds,
                id='map',
                className='map-container'
            ),
            className='order-1 col-12 col-md-8'
        ),
        html.Div(
            [
                color_mode_switch,
                control_section
            ],
            className='order-2 col-12 col-md-4 text-size'
        )
    ],
    className="custom-margin row",
    style={"font-family": "'Roboto', sans-serif"}
)
