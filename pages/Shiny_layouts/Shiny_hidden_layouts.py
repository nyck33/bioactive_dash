import json
import re
import pandas as pd
from dash import Dash, exceptions, no_update, callback_context
from dash.dependencies import Input, Output, State
from dash_utils.Dash_fun import apply_layout_with_auth
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
from mongoengine import connect
#from app import db
from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
        CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)
from models.model_nutrients import (
            ElementsRDI, VitaminsRDI, ElementsUpperRDI,
            VitaminsUpperRDI, MacronutrientsDistRange
        )
from models.model_infantsRDI import (
    InfantsElementsRDI, InfantsVitaminsRDI, InfantsMacroRDI, InfantsElementsUpperRDI,\
        InfantsVitaminsUpperRDI
)
from models.model_childrenRDI import (
    ChildrenElementsRDI, ChildrenVitaminsRDI, ChildrenMacroRDI, ChildrenElementsUpperRDI,\
        ChildrenVitaminsUpperRDI
)
from models.model_malesRDI import (
    MalesElementsRDI, MalesVitaminsRDI, MalesMacroRDI, MalesElementsUpperRDI, MalesVitaminsUpperRDI
)
from models.model_femalesRDI import (
    FemalesElementsRDI, FemalesVitaminsRDI, FemalesMacroRDI, FemalesElementsUpperRDI,\
        FemalesVitaminsUpperRDI
)
from models.model_pregnancyRDI import (
    PregnancyElementsRDI, PregnancyVitaminsRDI, PregnancyMacroRDI, PregnancyElementsUpperRDI,\
        PregnancyVitaminsUpperRDI
)
from models.model_lactationRDI import (
    LactationElementsRDI, LactationVitaminsRDI, LactationMacroRDI, LactationElementsUpperRDI,\
        LactationVitaminsUpperRDI
)

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
                editable=True,
                style_cell={'textAlign': 'left'},
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
                editable=True,
                style_cell={'textAlign': 'left'},
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
                editable=True,
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
            ),
            html.Br(),
            html.Div(
                id='err-nutrients-table'
            ),
            html.Pre(
                id='ctx-msg'
            ),
        ], width=12)
    ])
], id='cnf-layout', style={'display': 'none'})

cnf_totals_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            DataTable(
                id="cnf-totals-table",
                data=[],
                editable=True,
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
        ])
    ])
],id='cnf-totals-layout', style={'display': 'none'})

rdi_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="cnf-vs-rdi-one-elements"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-one-vitamins"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-one-macro"
            ),

        ], width=12)
    ])
], id='rdi-layout', style={'display': 'none'})

rdi_totals_layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="cnf-vs-rdi-totals-elements"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-totals-vitamins"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-totals-macro"
            ),

        ], width=12)
    ]),
    id='rdi-totals-layout', style={'display': 'none'}
)