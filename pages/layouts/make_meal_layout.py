import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
from flask_login import current_user


from dash_utils.Shiny_utils import (rdi_nutrients, rdi_modelnames_arr, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)


food_to_id_dict, food_names_arr, food_ids_arr = make_food_to_id_dict()


# injected layouts
cnf_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                id="chosen-food"  # shows full name in <H3>
            ),
            html.Div(
                id="test-out"
            ),
            html.Br(),
            DataTable(
                id="table-foodgroup-source",
                data=[],
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                    'textAlign': 'left'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)'
                }],
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                },
            ),
            html.Div(
                html.H5("Conversions Multipliers")
            ),
            html.Br(),
            DataTable(
                id="conversions-table",
                data=[],
                style_cell={'textAlign': 'left'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)'
                }],
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                },
            ),
            html.Div(
                html.H5("Nutrients")
            ),
            html.Br(),
            DataTable(
                id="nutrients-table",
                data=[],
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                },
                style_cell_conditional=[{
                    'if': {'column_id': c},
                    'textAlign': 'left'

                } for c in ['Name']
                ],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)',
                }],
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                },
            ),
            html.Br(),
            html.Div(
                id='err-nutrients-table'
            ),
            html.Pre(
                id='ctx-msg'
            ),
        ], width=6)
    ])
], id='cnf-layout', style={'display': 'block'})

cnf_totals_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            DataTable(
                id="cnf-totals-table",
                data=[],
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                },
                style_cell_conditional=[{
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['Name']
                ],
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)'
                }],
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                },
            )
        ], width=6)
    ])
],id='cnf-totals-layout', style={'display': 'none'})

