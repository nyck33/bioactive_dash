import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

my_meals_layout=dbc.Container([
    dbc.Row([
        dbc.Col([

        ], width=12)
    ]
    )
], id="my-meals-layout", style={'display': 'block'}
)