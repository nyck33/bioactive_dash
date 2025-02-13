"""
# -*- coding: utf-8 -*-
"""
#@author; Nobu Kim
from flask_login import current_user
import json
import re
import pandas as pd
from dash import Dash, exceptions, no_update, callback_context
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
import plotly.express as px
import plotly.graph_objects as go

from server import (db_mongo)
from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)

from dash_utils.make_meal_utils import nut_names_arr

# import the rdi csv table names and filenames arrs


from dash_utils.Shiny_utils import (rdi_nutrients, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

#import layouts
from .layouts.make_meal_layout import (cnf_layout, cnf_totals_layout)
from .layouts.bioactive_layout import (bioactive_layout)
from .layouts.rdi_charts_layout import (rdi_charts_layout)
#import callbacks
from .callbacks.make_meal_callbacks import (register_make_meal_callbacks)
from .callbacks.bioactive_callbacks import (register_bioactive_callbacks)
from .callbacks.rdi_charts_callbacks import (register_rdi_charts_callbacks)

#for Flask Login
import random
from flask_login import current_user
import time
from functools import wraps

from server import app
register_make_meal_callbacks(app)
register_rdi_charts_callbacks(app)


login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

location = dcc.Location(id='make-meal-url',refresh=True)


# used in layout for datalist
food_to_id_dict, food_names_arr, food_ids_arr = make_food_to_id_dict()

# dict of cnf nutrient names: nutrient units
nutrients = CNFNutrientName.objects
cnf_nutr_dict = {}
cnf_nutrient_names_all = []
cnf_nutrient_units_all = []
for n in nutrients:
    cnf_nutr_dict[str(n.name)] = str(n.unit)
    cnf_nutrient_names_all.append(str(n.name))
    cnf_nutrient_units_all.append(str(n.unit))

assert len(cnf_nutrient_names_all) == len(cnf_nutrient_units_all)
num_values = len(cnf_nutrient_names_all)
# make a base nutrients dataframe to cumulate into
nutrients_totals_dict = {
    "Name": cnf_nutrient_names_all,
    "Value": ["0" for i in range(num_values)],
    "Units": cnf_nutrient_units_all
}

controls_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Store(  # todo: hide dataframes as json
                id="hidden-conversions-df", storage_type='session'
            ),
            dcc.Store(
                id="hidden-nutrients-df", storage_type='session'
            ),
            dcc.Store(
                id="hidden-cumul-ingreds-df", storage_type='session'
            ),
            dcc.Store(
                id='hidden-total-nutrients-df', storage_type='session'

            ),
            dcc.Store(  # todo: trigger on selecting age and lifestage group
                id="hidden-rdi-df", storage_type='session'
            ),
            dcc.Store(
                id='nutrient-foods-store', storage_type='session'
            )

        ], width=12),
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Selected Ingredients"),
            DataTable(  # ingredient, amt, units
                id='cumul-ingreds-table',
                data=[],
                row_deletable=True,
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
            html.Div(id='cumul-ingreds-ui'),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("1. Choose Ingredient by Name"),
            html.Br(),
            dcc.Input(
                id="search-ingredient",
                list="food_names",
                placeholder='Enter food name',
                debounce=True,
                style={'width': '100%'}
            ),
            html.Datalist(
                id="food_names",
                children=[
                    html.Option(value=food) for food in food_names_arr
                ]
            ),
            html.Br(),
            dbc.Button(
                "Search Ingredient",
                id='search-ingredient-btn',
                color='primary'
            ),
            html.Br(),
            html.Label('Or Choose Ingredient by Nutrient'), #filter here for plant-based
            dcc.Dropdown(
                id='search-nutrient-foods',
                options=[{'label': nut, 'value': nut} for nut in nut_names_arr],
                value=nut_names_arr[0]
            ),

            html.Br(),
            dbc.Button(
                "Search by Nutrient",
                id='search-by-nut-btn',
                color='primary'
            ),
            html.Br(),
            html.Br(),
            dbc.Button(
                "get my alternates",
                id='get-alts-btn',
                color='warning'
            )
        ],width=6),
        dbc.Col([
            html.Div(
                id='alt-ingreds-display'
            ),
            DataTable(
                id="nutrient-foods-table",
                data=[],
                filter_action='native',
                # sort_action='native',
                # sort_mode='multi',
                column_selectable='single',
                row_selectable=False,
                selected_columns=[],
                selected_rows=[],
                page_action='native',
                page_current=0,
                page_size=8,
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                },
                style_cell_conditional=[{

                    'textAlign': 'left'

                } for c in ['Name']  # todo: change this
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
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("2. Amount Units"),
            dcc.Dropdown(
                id="units-dropdown",
                style={'width': '75%'}
            ),
            html.Br(),
            html.Label("3. Quantity"),
            html.Br(),
            dcc.Input(
                id="numerical-amount", type="number",
            ),
            html.Br(),
            dbc.Button(
                "Update Nutrient Table",
                id="update-nut-table-btn",
                color='success'
            ),
            html.Br(),
            html.Br(),
            dbc.Button(
                "Add to Recipe",
                id='add-ingredient',
                color='success',
                n_clicks=0
            ),
            dbc.Button(
                "Remove Ingredient",
                id="remove-ingredient",
                color='danger',
                n_clicks=0
            )
        ], width=6),

    ]),

    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id="radio-display-type",
                options=[
                    {'label': 'Nutrient Table for ingredient', 'value': 'cnf-table'},
                    {'label': 'Nutrient Table for all ingredients', 'value': 'cnf-totals-table'},
                    {'label': 'vs RDI charts', 'value': 'rdi-charts'},
                    {'label': 'Bioactive Compounds', 'value': 'bioactive-table'},
                    {'label': 'My Meals', 'value': 'my-meals'}
                ],
                value='cnf-table'
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                id="data-layout"
            )
        ], width=12)
    ])

], id="controls-layout", style={'display': 'block'}

)


def layout():
    full_layout = html.Div([controls_layout, cnf_layout, cnf_totals_layout, rdi_charts_layout])

    return full_layout




'''
# replaced with D
            dcc.Input(
                id="search-nutrient-foods",
                list="nutrient_names",
                placeholder='Enter nutrient name',
                debounce=True,
                style={'width': '100%'}
            ),
            html.Datalist(
                id="nutrient_names",
                children=[
                    html.Option(value=nutrient) for nutrient in nut_names_arr
                ]
            ),
'''

