import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
import plotly.express as px
import plotly.graph_objects as go


from dash_utils.Shiny_utils import (rdi_nutrients, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

food_to_id_dict, food_names_arr, food_ids_arr = make_food_to_id_dict()

rdi_charts_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                dcc.Graph(
                    id="cnf-vs-rdi-one-elements"
                )
            ),
            html.Div(
                dcc.Graph(
                    id="cnf-vs-rdi-one-vitamins"
                )
            ),
            html.Div(
                dcc.Graph(
                    id="cnf-vs-rdi-one-macro"
                )
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                dcc.Graph(
                    id="cnf-vs-rdi-totals-elements"
                )
            ),
            html.Div(
                dcc.Graph(
                    id="cnf-vs-rdi-totals-vitamins"
                )
            ),
            html.Div(
                dcc.Graph(
                    id="cnf-vs-rdi-totals-macro"
                )
            )
        ], width=12)
    ]),
], id='rdi-charts-layout', style={'display':'none'})