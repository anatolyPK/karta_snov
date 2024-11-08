import dash_bootstrap_components as dbc
from dash import Dash

from src.callbacks import *
from src.page import layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

server = app.server

app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0')
