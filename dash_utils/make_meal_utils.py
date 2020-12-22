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
from flask_login import current_user
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# for foods by nutrients
nut_engine = create_engine("mysql+pymysql://root:tennis33@localhost/dashcnf?charset=utf8mb4")#, echo=True)
nut_table_names = nut_engine.table_names()
nut_names_arr = [nut_name.replace("_foods", "") for nut_name in nut_table_names
                    if 'user' not in nut_name]

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
    get_df_cols, strip_units, get_calories_per_day,
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

#utilities
def get_target_col(cnf_nut, cols):
    """
    looks for cnf_nut in rdi col names
    but rdi name is shorter
    """
    target_col = ""
    for col in cols:
        if cnf_nut in str(col).lower():
            target_col = col
            break
    return target_col



def get_lifestage_idxs(usr_type):
    # index into rdi_elements_df and get rdi value
    start_idx = lifestage_idx_dict[usr_type]
    end_idx = len(rdi_macros_df.index)
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
    todo: dicts_arr is missing rdi in cnf matches
    '''
    for match_nuts in dicts_arr:
        cnf = match_nuts[0]
        cnf_nut = list(cnf.keys())[0]
        if cnf_nut != nut_name:
            continue
        cnf_units = list(cnf.values())[0]
        #print(cnf_nut, cnf_units)
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

def preprocess_cnf_nuts(nut):
    if nut == "fat (total lipids)":
        nut = 'fat'
    elif nut == "carbohydrate, total (by difference)":
        nut = 'carbohydrate'
    elif nut == "fibre, total dietary":
        nut = 'fiber'
    elif nut == "fatty acids, polyunsaturated, 18:2undifferentiated, linoleic, octadecadienoic":
        nut = 'linoleic acid'
    elif nut == 'fatty acids, polyunsaturated, 18:3undifferentiated, linolenic, octadecatrienoic':
        nut = 'alpha-linolenic acid'
    elif nut == "vitamin d (d2 + d3)":
        nut = 'vitamin d'
    elif nut == "niacin (nicotinic acid) preformed":
        nut = 'niacin'
    elif nut == "dietary folate equivalents":
        nut = 'folate'
    elif nut == 'vitamin b12, added':
        nut = 'vitamin b12'
    elif nut == 'choline, total':
        nut = 'choline'
    elif nut == 'alpha-tocopherol':
        nut = 'vitamin e'
    elif nut == 'retinol':
        nut = 'vitamin a'
    elif nut == 'vitamin b-6':
        nut = 'vitamin b6'
    elif nut == 'vitamin b-12':
        nut = 'vitamin b12'

    return nut

def color_bars(df):
    '''
    elif 80. > val >= 60.:
        colors.append('rgb(0,255,0)')
    elif 60. > val >= 40.:
        colors.append('rgb(0,0,255)')
    '''
    colors = []
    cols = list(df.columns)
    for col in cols:
        val = float(df.loc[0,col])
        if val >= 100.:
            colors.append('rgb(255,0,0)')
        elif 100. > val >= 40.:
            colors.append('rgb(0,0,255)')

        else:
            colors.append('rgb(192,192,192)')
    return colors

meal_type_arr = ['breakfast', 'lunch', 'dinner', 'brunch', 'snack',
                 'dessert', 'cheat']

from datetime import date, datetime


def make_cumul_ingreds_ui():
    """
    build Datatable, save meal btn, dropdown for meal type,
    add textarea for description or title for meal to use on nutritionix api
    and quick reference on my_meals when pulling from mysql
    """
    today = datetime.today().strftime('%Y-%m-%d')
    date_arr = today.split('-')
    year = int(date_arr[0])
    month = int(date_arr[1])
    day = int(date_arr[2])

    # up to a year ago
    now = datetime.now()
    last_year = now.year - 1
    next_year = now.year + 1

    cumul_ingreds_ui = html.Div([
        #datatable fits here
        dcc.Dropdown(
            id='meal-type-dropdown',
            options=[{'label':meal, 'value': meal} for meal in meal_type_arr],
            value=meal_type_arr[0]
        ),
        html.Br(),
        html.Label('Enter description of recipe or meal'),
        dcc.Textarea(
            id='meal-desc',
            placeholder='mabo tofu with plant-based beef, white rice, miso soup',
            style={'width': '100%', 'height': 100}
        ),
        dcc.DatePickerSingle(
            id='meal-date-picker',
            min_date_allowed=date(last_year, 1, 1),
            max_date_allowed=date(next_year, 12, 31),
            initial_visible_month=date(year, month, day),
            date=date(year, month, day)
        ),
        html.Div(
            html.P(
                id='save-confirm-msg'
            )
        ), #see save details here before button
        dbc.Button(
            "Save Meal",
            id='save-meal-btn'
        )
    ])

    return cumul_ingreds_ui


def fill_nut_df(nut_type, start_idx, end_idx, usr_life_stg,
                 cnf_nut, cnf_amt, multiplier,
                 the_df, #elems, vits or macro to fill with percentages
                usr_type, usr_age, usr_active_lvl,
                num_days=1.):

    #from macro-distrange, percent fat of energy
    max_fat = .3  # default for adults is 20 to 35%
    age_num = int(usr_age)
    if age_num <= 3:  # 30 to 40%
        max_fat = .4
    elif 3 < age_num <= 18:  # 25 to 35%
        max_fat = .35
    elif age_num > 18:
        max_fat = .3

    #choose rdi_df by nut_type
    rdi_df = None
    if nut_type == "element":
        rdi_df = rdi_elems_df.copy()
    elif nut_type == "vitamin":
        rdi_df = rdi_vits_df.copy()
    elif nut_type == "macronutrient":
        rdi_df = rdi_macros_df.copy()

    #multiply cells by num days,
    rdi_df = rdi_df.astype(str)
    #print(f'rdi_df before:\n {rdi_df}, {rdi_df.dtypes}')

    cols = list(rdi_df.columns)
    key_cols = cols[1:]
    for idx, row in rdi_df.iterrows():
        for col in key_cols:

            # get curr_val in rdi_df
            curr_val = rdi_df.loc[idx, col]
            #print(f'curr_val: {curr_val}, idx: {idx}, col: {col}')
            if curr_val == 'ND' or curr_val == 'nan' or curr_val == 'None':
                continue
            else:
                curr_val = float(curr_val) * num_days
                rdi_df.loc[idx, col] = curr_val
    #print(f'rdi_df after:\n {rdi_df}, {rdi_df.dtypes}')

    df = the_df.copy()
    # get slice of df
    portion = rdi_df.iloc[start_idx:end_idx, :].astype(str)
    row = portion[portion['Life-Stage Group'] == usr_life_stg]
    cols = list(row.columns)
    target_col = get_target_col(cnf_nut, cols)
    target_val = row[target_col].item()
    if target_val != 'nan' and target_val != 'ND':
        val = float(row[target_col].item())
    # todo: fix this Z
    elif target_val == "ND":
        """
        9 calories per fat gram
        """
        calories_per_fatg = 9.
        # get calorie value
        calories_per_day = get_calories_per_day(usr_type, usr_age, usr_active_lvl)
        # mult calories per day from those allowed from fat from RDI and num_days
        fat_cals_per_period = (float(calories_per_day) * num_days) * max_fat
        percent = ((float(cnf_amt) * multiplier
                    * calories_per_fatg) / fat_cals_per_period) * 100.
        # index into elems_df and enter percent
        plot_cols = list(df.columns)
        target_col = get_target_col(cnf_nut, plot_cols)
        df.loc[0, target_col] = percent

        return df
    else:  # todo: this assumes when nan that any intake fulfills rda
        val = cnf_amt #not multiplied by num_days

    percent = ((cnf_amt * multiplier) / val) * 100.
    # index into elems_df and enter percent
    plot_cols = list(df.columns)
    target_col = get_target_col(cnf_nut, plot_cols)
    df.loc[0, target_col] = percent

    return df



'''
html.H3("Recipe Ingredients"),
        html.Br(),
        DataTable(  # ingredient, amt, units
            id='cumul-ingreds-table',
            data=df.to_dict('records'),
            columns=[{"name":i, "id":i} for i in df.columns],
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
        html.Br(),
'''