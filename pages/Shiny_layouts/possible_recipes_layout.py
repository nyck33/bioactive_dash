import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

possible_recipes_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                "Bon API or nutritionix, etc choose one",
                id="recipes-api-controls"
            )
        ], width=12)
    ])
], id='possible-recipes-layout', style={'display': 'none'})