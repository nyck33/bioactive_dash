import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

user_prof_layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            # todo: show warnings if over RDI and display red if over upper RDI
            html.Label("Enter age"),
            dcc.Input(
                id="age-input", type="number", value='30',
                debounce=True
            ),
            html.Br(),
            html.Label("Select gender"),
            dcc.RadioItems(
                options=[
                    {'label': 'male', 'value': 'Males'},
                    {'label': 'female', 'value': 'Females'},
                    {'label': 'pregnant', 'value': 'Pregnancy'},
                    {'label': 'lactating', 'value': 'Lactation'}
                ],
                value='Females'
            ),
            html.Br(),

        ], width=12)
    ])
], id="user-prof-layout", style={'display': 'block'})