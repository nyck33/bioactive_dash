import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

cnf_vs_rdi_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="cnf-vs-rdi-recipe-elements"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-recipe-vitamins"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-recipe-macro"
            ),

        ], width=12)
    ])
], id='cnf-vs-rdi-recipe-layout', style={'display': 'none'})