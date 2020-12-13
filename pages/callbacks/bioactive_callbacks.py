# -*- coding: utf-8 -*-
"""
@author; Nobu Kim
"""
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

from dash_utils.Shiny_utils import (rdi_nutrients, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)
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


def register_bioactive_callbacks(app):
    pass