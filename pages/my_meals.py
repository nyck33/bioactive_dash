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
from dash_utils.Dash_App_utils import (table_names_arr, csv_names_arr, make_dataframes,
                                            make_table, make_figure)

from dash_utils.Shiny_utils import (rdi_nutrients, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

from .callbacks.my_meals_callbacks import (register_my_meals_callbacks)
from .layouts.my_meals_layout import (my_meals_layout,
                                      period_layout,
                                    per_selection_layout,
                                    alt_ingreds_layout)
from server import app
register_my_meals_callbacks(app)

login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

location = dcc.Location(id='my-meals-url',refresh=True)

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


def layout():
    full_layout = html.Div([
        my_meals_layout,
        period_layout,
        per_selection_layout,
        alt_ingreds_layout
    ])
    return full_layout