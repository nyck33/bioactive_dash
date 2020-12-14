"""
Query for meals and ingreds in date range
Show one meal at a time
Return Datatable of meal_id, meal_type, date
"""
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
from flask_login import current_user

my_meals_layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("View Past Meals"),

        ], width=12)
    ]
    )
], id="my-meals-layout", style={'display': 'block'}
)