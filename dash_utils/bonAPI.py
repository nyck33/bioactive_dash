# -*- coding: utf-8 -*-
"""
@author; Nobu Kim
"""
import json
import re
import pandas as pd
from dash import Dash, exceptions, no_update, callback_context
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

import plotly.graph_objects as go

from utilities.config import engine as engine
from flask_login import current_user
from sqlalchemy import select, Table, Column, String, MetaData
from datetime import datetime, date

from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)
from dash_utils.make_meal_utils import nut_engine, make_cumul_ingreds_ui

from dash_utils.Shiny_utils import (rdi_nutrients, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)
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
nuts_totals_dict = {
    "Name": cnf_nutrient_names_all,
    "Value": ["0" for i in range(num_values)], # 0 should be str
    "Units": cnf_nutrient_units_all
}

#######################################################################
from dash_utils.nut_match_cnf_rdi import (
    # {nuts:units}
    rdi_elems_dict, rdi_vits_dict, rdi_macros_dict,
    df_dict,
    # {nuts:units}
    cnf_nuts_dict,
    rdi_units_dict,
    # compared cnf_nuts_dict v. rdi_units_dict
    exacts, converts, not_match,
    #functions
    get_df_cols, strip_units,
    #arrs of [{cnf_nut:cnf_unit}, {rdi_nut: rdi_units}]
    cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts
)

rdi_elems_df = df_dict['elements_rdi']
rdi_vits_df = df_dict['vitamins_rdi']
rdi_macros_df = df_dict['macronutrients_rdi']

#set up indices for lifestage groups
infants_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Infants'][0]
child_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Children'][0]
male_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Males'][0]
fem_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Females'][0]
preg_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Pregnancy'][0]
lact_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Lacation'][0]

#except for last go to the next, 0 3 6 13 20 24
lifestage_idxs = [infants_idx, child_idx, male_idx, fem_idx, preg_idx, lact_idx]
#todo: must match keys with person_type in user table
lifestage_idx_dict = {
    'infant': infants_idx, 'child':child_idx, 'male':male_idx, 'female':fem_idx,
    'pregnant': preg_idx, 'lactating':lact_idx
}
############################################################################
#utilities import
from dash_utils.make_meal_utils import (get_target_col, get_lifestage_idxs,
                                        find_type, preprocess_cnf_nuts,
                                        color_bars)
###########################################################################
"""
example request:
https://www.bon-api.com/api/v1/ingredient/alternatives/mozzarella, 
sausages, pizza crust/?allergies=lactose_intolerance&diet=vegan&composition=total_fat,sugar,protein,calcium,iron,vit_b9,cobalamin_vit_b12,water_content
response as dict:
 {'request': {'allergies': ['lactose_intolerance'], 'data_notes': 
 'All values are per 100 grams of the respective ingredient', 'diet': 'Vegan', 
 'language': 'en', 'provided_ingredients': ['mozzarella', ' sausages', 
 ' pizza crust']}, 
 'response': {'alerts': {'ingredients_not_found': 
 ['pizza crust']}, '
 allergens_1': ['Gluten Allergy', 'Tree Nut Allergy', 
 'Soy Allergy'], 
 'allergens_2': ['Celery Allergy', 'Crustacean Allergy', 
 'Egg Allergy', 'Fish Allergy', 'Gluten Allergy', 'Lactose Intolerance', 
 'Lupin Allergy', 'Milk Allergy', 'Mollusc Allergy', 'Mustard Allergy', 
 'Peanut Allergy', 'Sesame Allergy', 'Soy Allergy', 'Tree Nut Allergy', 
 'Wheat Allergy'], 
 'diet_1': [], 
 'diet_2': ['Pescetarian', 'Vegetarian', 'Vegan'], 
 'matched_ingredients': ['mozzarella  ----->  mozzarella', 
 'sausages  ----->  pork_sausage'], 
 'updated_ingredients': 
 ['Coconut Based Mozzarella (previously: mozzarella)', 
 'Soy Based Ham (previously:  sausages)', 'pizza crust']}}
"""
###########################################################################
import pandas as pd
import requests
import json
from .bon_params import allergies_dict, diet_dict, prep_dict


def get_bon_alt_ingreds(ingreds_str, allergies=None, diet=None, composition=''):
    api_token = 'c61bd3c92b76cdb4867d02f48ea73ede8d5ccf4b'
    api_url_base = 'https://www.bon-api.com/api/v1/ingredient/alternatives/'

    #  *** BONAPI COMMENT ***
    # Bearer not recognised - should be 'Token'
    headers = {'Authorization': f'Token {api_token}'}

    api_url = f'{api_url_base}{ingreds_str}' if allergies is None \
        else f'{api_url_base}{ingreds_str}/?{allergies}&{diet}'#&{composition}'

    print(api_url)
    response = requests.get(api_url, headers=headers)
    #  *** BONAPI COMMENT ***
    # Recommend to always return full text as we handle errors and provide comments as to why the error may be occuring
    text = json.dumps(response.json(), sort_keys=True, indent=1)
    return text


def make_alt_ingreds_ui(ingreds_table):
    ingreds_tbl_ui = html.Div([
        html.H5("Select ingredient for nutrients and alternatives"),
        ingreds_table,
        html.Label('Enter ingredients keywords to search'),
        dcc.Textarea(
            id='alt-ingreds-text',
            placeholder='chicken breast, mozzarella, ground beef...',
            style={'width': '100%', 'height': 200},
        ),
        html.Label('select allergies if any:'),
        dcc.Dropdown(
            id='allergies-dropdown',
            options=[
                {'label': k, "value": v} for k,v in allergies_dict.items()
            ],
            value=list(allergies_dict.keys())[0],
            multi=True
        ),
        html.Label('select your diet preference:'),
        dcc.Dropdown(
            id='diet-dropdown',
            options=[
                {'label': k, 'value': v} for k,v in diet_dict.items()
            ],
            value=list(diet_dict.keys())[0]
        ),
        dbc.Button(
            "search alternatives",
            id='search-alt-btn',
            color='primary'
        )

    ])

    return ingreds_tbl_ui


def make_save_alts_ui(alt_ingreds_str, alt_ingreds_arr_json):
    alt_ingreds_ui = html.Div([
        dcc.Store(
            id='alt-ingreds-json',
            storage_type='session',
            data=alt_ingreds_arr_json
        ),
        html.Div(
            html.P(
                alt_ingreds_str,
                id='alt-ingreds-str'
            )
        ),
        dbc.Button(
            "save alternates",
            id='save-alts-btn',
            color='primary'
        ),
        html.Div(
            id='alts-saved-msg'
        )
    ])

    return alt_ingreds_ui
