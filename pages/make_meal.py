"""
# -*- coding: utf-8 -*-
"""
#@author; Nobu Kim

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
#todo: move to app
#connect to Mongo
#connect('cnf')
from server import db_mongo

from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)
from models.model_nutrients import (
    ElementsRDI, VitaminsRDI, ElementsUpperRDI,
    VitaminsUpperRDI, MacronutrientsDistRange
)
from models.model_infantsRDI import (
    InfantsElementsRDI, InfantsVitaminsRDI, InfantsMacroRDI, InfantsElementsUpperRDI, \
    InfantsVitaminsUpperRDI
)
from models.model_childrenRDI import (
    ChildrenElementsRDI, ChildrenVitaminsRDI, ChildrenMacroRDI, ChildrenElementsUpperRDI, \
    ChildrenVitaminsUpperRDI
)
from models.model_malesRDI import (
    MalesElementsRDI, MalesVitaminsRDI, MalesMacroRDI, MalesElementsUpperRDI, MalesVitaminsUpperRDI
)
from models.model_femalesRDI import (
    FemalesElementsRDI, FemalesVitaminsRDI, FemalesMacroRDI, FemalesElementsUpperRDI, \
    FemalesVitaminsUpperRDI
)
from models.model_pregnancyRDI import (
    PregnancyElementsRDI, PregnancyVitaminsRDI, PregnancyMacroRDI, PregnancyElementsUpperRDI, \
    PregnancyVitaminsUpperRDI
)
from models.model_lactationRDI import (
    LactationElementsRDI, LactationVitaminsRDI, LactationMacroRDI, LactationElementsUpperRDI, \
    LactationVitaminsUpperRDI
)

# import the rdi csv table names and filenames arrs
from dash_utils.Dash_App_utils import (table_names_arr, csv_names_arr, make_dataframes,
                                            make_table, make_figure)

from dash_utils.Shiny_utils import (rdi_nutrients, rdi_modelnames_arr, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

#from .layouts.Shiny_hidden_layouts import (cnf_layout, cnf_totals_layout)
from .layouts.make_meal_layout import (cnf_layout, cnf_totals_layout)
from .callbacks.make_meal_callbacks import (register_make_meal_callbacks)
#for Flask Login
import random
from flask_login import current_user
import time
from functools import wraps

from server import app
register_make_meal_callbacks(app)


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
                id="hidden-conversions-df", storage_type='memory'
            ),
            dcc.Store(
                id="hidden-nutrients-df", storage_type='memory'
            ),
            dcc.Store(
                id="hidden-cumul-ingreds-df", storage_type='memory'
            ),
            dcc.Store(
                id='hidden-total-nutrients-df', storage_type='memory'

            ),
            dcc.Store(  # todo: trigger on selecting age and lifestage group
                id="hidden-rdi-df", storage_type='memory'
            ),

        ], width=12),
    ]),
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

            html.Label("1. Choose Ingredient"),
            html.Br(),
            dcc.Input(
                id="search-ingredient",
                list="food_names", placeholder='Enter food name',
                debounce=True,
                style={'width': '50%'}
            ),
            html.Datalist(
                id="food_names", children=[
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
            html.Label("2. Amount Units"),
            dcc.Dropdown(
                id="units-dropdown",
                style={'width': '40%'}
            ),
            html.Br(),
            html.Label("3. Quantity"),
            dcc.Input(
                id="numerical-amount", type="number",
            ),
            html.Br(),
            dbc.Button(
                "Update Nutrient Table",
                id="update-nut-table-btn",
                color='success'
            ),
            dbc.Button(
                "Show %RDI for ingredient",
                id='%rdi-ingredient-btn',
                color='warning'
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
            ),
            dcc.RadioItems(
                id="radio-display-type",
                options=[
                    {'label': 'Nutrient Tables & RDI for ingredient', 'value': 'cnf-table'},
                    {'label': 'Nutrient Tables & RDI for all ingredients', 'value': 'cnf-totals-table'},
                ],
                value='cnf-table'
            )

        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Selected Ingredients"),
            DataTable(  # ingredient, amt, units
                id='cumul-ingreds-table',
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
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                id="data-layout"
            )
        ], width=12)
    ])

], id="controls-layout",
    style={'display': 'block'},

)


def layout():
    full_layout = html.Div([controls_layout, cnf_layout, cnf_totals_layout])

    return full_layout



