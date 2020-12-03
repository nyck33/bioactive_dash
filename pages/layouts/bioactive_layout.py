import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

bioactive_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                "Search MySQL database for matching terms",
                id="search-db-display"
            )
        ], width=12)
    ])
], id='bioactive-layout', style={'display': 'none'})