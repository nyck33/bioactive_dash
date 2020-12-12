"""
callbacks related to making charts and graphs for
cnf intake vs rdi comparison
Default lifestage grp:
age = Column(Integer, nullable=False) #def 35
gender = Column(Integer, nullable=False) #def 0=female
#"female, 31 to 50 y"
life_stage_grp = Column(String(255), nullable=False)
Get user info
"""
# -*- coding: utf-8 -*-
"""
@author; Nobu Kim
"""
from flask_login import current_user


import json
import re
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from dash import Dash, exceptions, no_update, callback_context
from dash.dependencies import Input, Output, State
from dash_utils.Dash_fun import apply_layout_with_auth
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
from dash_table import DataTable
from mongoengine import connect

from dash_utils.Shiny_utils import (rdi_nutrients, rdi_modelnames_arr, make_food_to_id_dict, get_unit_names,
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
nuts_totals_dict = {
    "Name": cnf_nutrient_names_all,
    "Value": ["0" for i in range(num_values)],
    "Units": cnf_nutrient_units_all
}
'''
exacts are matches of name and units,
converts need changes in units
not_match is a long list of cnf_nuts not in rdi
'''
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
'''
for each element/vitamin/macro, check if it's in {found}, if so, add it to
graph
cnf based dataframe of food or recipe is sent to callback, compare that with rdi
'''
###########################################################################
#utilities
def get_target_col(cnf_nut, cols):
    target_col = ""
    for col in cols:
        if cnf_nut in str(col).lower():
            target_col = col
            break
    return target_col


def get_lifestage_idxs(usr_type):
    # index into rdi_elements_df and get rdi value
    start_idx = lifestage_idx_dict[usr_type]
    if usr_type != 'lactating':
        for i in range(len(lifestage_idxs)):
            if start_idx == lifestage_idxs[i]:
                end_idx = lifestage_idxs[i + 1]
                break
    else:
        end_idx = len(rdi_macros_df.index)

    return start_idx, end_idx


def find_type(nut_name, dicts_arr):
    '''
    dicts_arr: cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts
    '''
    for match_nuts in dicts_arr:
        cnf = match_nuts[0]
        cnf_nut = list(cnf.keys())[0]
        if cnf_nut != nut_name:
            continue
        cnf_units = list(cnf.values())[0]
        # print(cnf_nut, cnf_units)
        rdi = match_nuts[1]
        rdi_nut = list(rdi.keys())[0]
        rdi_units = list(rdi.values())[0]
        for rdi_n, rdi_u in rdi_elems_dict.items():
            if cnf_nut in rdi_n:
                multiplier = convert_units(cnf_units, rdi_u)
                return 'element', rdi_n, multiplier
        for rdi_n, rdi_u in rdi_vits_dict.items():
            if cnf_nut in rdi_n:
                multiplier = convert_units(cnf_units, rdi_u)
                return 'vitamin', rdi_n, multiplier
        for rdi_n, rdi_u in rdi_macros_dict.items():
            if cnf_nut in rdi_n:
                multiplier = convert_units(cnf_units, rdi_u)
                return 'macronutrient', rdi_n, multiplier

    return "", "", ""


def convert_units(cnf_units, rdi_units):
    '''
    return multiplier for the cnf nut unit from ingred or recipe df
    '''
    if cnf_units == 'mg/d' and rdi_units == 'ug/d':
        return 1000.
    elif cnf_units == 'mg/d' and rdi_units == 'g/d':
        return 0.001
    elif cnf_units == 'ug/d' and rdi_units == 'mg/d':
        return 0.001
    elif cnf_units == 'g/d' and rdi_units == 'mg/d':
        return 1000.
    elif cnf_units == 'mg/d' and rdi_units == 'g/d':
        return 0.001
    # no conversion return 1
    return 1.
###########################################################################
def register_rdi_charts_callbacks(app):
    # update nuts_table btn updates rdi-one figures
    #todo: for each nutrient in the ingred_df, search rdi's for matches of just the name,
    # look at units, convert to the same, get a percentage for chart y-val
    # chart x-val's are the nutrients: elements, vitamins, macros
    '''
    #could take out row, fill it and make dataframe
    elem_row = rdi_elements_df[rdi_elements_df['Life-Stage Group']] = usr_life_stg
    vit_row = rdi_vitamins_df[rdi_vitamins_df['Life-Stage Group']] = usr_life_stg
    macro_row = rdi_macros_df[rdi_macros_df['Life-Stage Group']] = usr_life_stg
    '''
    @app.callback(
        [Output('cnf-vs-rdi-one-elements', 'figure'),
        Output('cnf-vs-rdi-one-vitamins', 'figure'),
         Output('cnf-vs-rdi-one-macro', 'figure')],
        [Input('hidden-nutrients-df', 'data')]
    )
    def update_ingred_charts(ingred_json):
        usr_life_stg = ''
        usr_type = ''
        if current_user.is_authenticated:
            usr_life_stg = current_user.lifestage_grp
            usr_type = current_user.person_type

        if ingred_json is None:
            return no_update, no_update, no_update
        # Name Value Units
        ingred_df = pd.read_json(ingred_json, orient='split')
        print(ingred_df)
        # df of nuts by category with field values as %
        elems_df = pd.DataFrame(columns=list(rdi_elems_dict.keys()))
        vits_df = pd.DataFrame(columns=list(rdi_vits_dict.keys()))
        macros_df = pd.DataFrame(columns=list(rdi_macros_dict.keys()))

        #calculate percentages
        # get row in each df elem_rdi, vit_rdi, macros_rdi
        for idx, row in ingred_df.iterrows():
            cnf_nut = row['Name'].lower()
            cnf_amt = float(row['Value'])
            cnf_units = row['Units']
            nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_elems_dicts)
            if nut_type=="":
                nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_vits_dicts)
            if nut_type=="":
                nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_macros_dicts)

            # get start and exclusive end idx of rdi_df
            start_idx, end_idx = get_lifestage_idxs(usr_type)
            if nut_type =='element':
                # get slice of df
                portion = rdi_elems_df.iloc[start_idx:end_idx, :]
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                val = float(row[target_col].item())
                percent = (cnf_amt * multiplier) / val
                # index into elems_df and enter percent
                plot_cols = elems_df.columns
                target_col = get_target_col(cnf_nut, plot_cols)
                elems_df.loc[0, target_col] = percent
            elif nut_type == 'vitamin':
                # get slice of df
                portion = rdi_vits_df.iloc[start_idx:end_idx, :]
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                val = float(row[target_col].item())
                percent = (cnf_amt * multiplier) / val
                # index into vits_df and enter percent
                plot_cols = vits_df.columns
                target_col = get_target_col(cnf_nut, plot_cols)
                vits_df.loc[0, target_col] = percent
            elif nut_type == 'macronutrient':
                # get slice of df
                portion = rdi_macros_df.iloc[start_idx:end_idx, :]
                row = portion[portion['Life-Stage Group']==usr_life_stg]
                cols= list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                val = float(row[target_col].item())
                percent = (cnf_amt * multiplier) / val
                #index into macros_df and enter percent
                plot_cols = macros_df.columns
                target_col = get_target_col(cnf_nut, plot_cols)
                macros_df.loc[0, target_col] = percent

        fig_elems = px.bar(elems_df, x=elems_df.columns.tolist(), y=elems_df.iloc[0])
        fig_vits = px.bar(vits_df, x=vits_df.columns.tolist(), y=vits_df.iloc[0])
        fig_macros = px.bar(macros_df, x=macros_df.columns.tolist(), y=macros_df.iloc[0])

        return fig_elems, fig_vits, fig_macros

    @app.callback(
        [Output('cnf-vs-rdi-totals-elements', 'figure'),
         Output('cnf-vs-rdi-totals-vitamins', 'figure'),
         Output('cnf-vs-rdi-totals-macro', 'figure')],
        [Input('hidden-total-nutrients-df', 'data')]
    )
    def update_recipe_charts(total_nuts_json):
        pass