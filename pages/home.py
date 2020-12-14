import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
import time

from server import app
from .layouts.user_prof_layout import (user_prof_layout,
person_type_arr, life_stage_arr)

from .callbacks.home_callbacks import register_home_callbacks
register_home_callbacks(app)

home_login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

home_layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='home-url', refresh=True),
                html.Div(id='home-login-trigger', style=dict(display='none')),

                html.H1('Micronutrients and Bioactive Compounds'),
                html.Br(),

                html.H5('Eat to Live not Live to Eat'),
                html.Br(),

                html.Div(id='home-test-trigger'),
                html.Div('before update', id='home-test')
            ],
            width=12
        )
    )
])

save_layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div(
                id='save-confirm-out'
            )
        ], width=6)
    ])
)

def layout():
    full_layout = html.Div([home_layout, user_prof_layout, save_layout])
    return full_layout


