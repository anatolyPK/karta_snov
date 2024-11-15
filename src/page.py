from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_leaflet as dl

from src.text import dropdown_text


image_path = "assets/karta_snov_50000.webp"
image_bounds = [
    [54.6480, 17.9904],
    [54.8458, 18.25950]
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
                'target': [],
                'road': []
            }
        ),
        html.Div(
            "Кликните на карту, чтобы получить координаты.",
            id='output-coordinates',
            className='custom-margin-top'
        ),
        html.Div(
            "Кликните на первый объект, а затем на второй для нахождения расстояния и магнитного азимиута между "
            "двумя объектами",
            id='output-distance-and-azimuth',
            className='custom-margin-top'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Определение магнитного азимута по дирекционному углу"),
                        dbc.Input(
                            placeholder="Введите значение ДУ",
                            type="text",
                            id='azimuth_input',
                            className='text-size'
                        )
                    ],
                    className='custom-margin-top'
                ),
                html.Div(id='azimuth-answer', className='custom-margin-top')
            ],
            id='output-azimuth',
            className='custom-margin-top'
        ),
        html.Div(
            [
                html.Div('Последовательно кликайте на точки маршрута', className='custom-margin-top'),
                html.Div(id='road-scheme-table', className='custom-margin-top')
            ],
            id='road-scheme-output',
            className='custom-margin-top'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Label("Поддерживаются следующие масштабы: 1:500000, 1:200000, 1:100000, 1:50000"),
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

choose_task = html.H2('Выберите задание:', className='text-size-h-2 custom-margin-top')

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch(id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ],
    className='d-flex justify-content-end custom-margin'
)

footer = html.Div(
    [
        html.Footer(
            [
                html.Div(
                    [
                        html.Span(
                            "Нашли ошибку? Напишите мне об этом!",
                            className="mb-3 mb-md-0 text-body-secondary align-items-center"
                        )
                    ],
                    className='col-md-4 d-flex align-items-center'
                ),
                color_mode_switch,
                html.Ul(
                    [
                        html.Li(
                            [
                                html.A(
                                    [
                                        html.I(className="fab fa-telegram footer-i-size")
                                    ],
                                    className="text-body-secondary",
                                    href="https://t.me/votetalal",
                                    target="_blank"
                                )
                            ],
                            className="ms-3"
                        ),
                        html.Li(className="ms-3", children=[
                            html.A(className="text-body-secondary", href="mailto:serff09@rambler.ru", children=[
                                html.I(className="fas fa-envelope footer-i-size")
                            ])
                        ])
                    ],
                    className="nav col-md-4 justify-content-end list-unstyled d-flex"
                ),
            ],
            className="d-flex flex-wrap justify-content-between align-items-center custom-padding-top border-top "
                      "custom-margin-footer"
        )
    ],
    className="custom-margin text-size"
)

layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    'Учебная топографическая карта СНОВ У-34-37-В',
                    className='d-flex justify-content-center text-center h1-size'
                ),
                html.Div(
                    dl.Map(
                        dl.ImageOverlay(url=image_path, bounds=image_bounds),
                        center=center,
                        zoom=12,
                        style={'width': '100%', 'cursor': 'crosshair'},
                        bounds=image_bounds,
                        id='map',
                        className='map-container',
                        attributionControl=False
                    ),
                    className='order-1 col-12 col-md-8'
                ),
                html.Div(
                    [
                        choose_task,
                        control_section
                    ],
                    className='order-2 col-12 col-md-4 text-size'
                )
            ],
            className="custom-margin row",
        ),
        footer
    ]
)
