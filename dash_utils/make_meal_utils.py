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

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql

nut_engine = create_engine("mysql+pymysql://root:tennis33@localhost/dashcnf?charset=utf8mb4")#, echo=True)

nut_table_names = nut_engine.table_names()

#nutrient names from the above

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

def preprocess_cnf_nuts(nut):
    if nut == "fat (total lipids)":
        nut = 'fat'
    elif nut == "carbohydrate, total (by difference)":
        nut = 'carbohydrate'
    elif nut == "fibre, total dietary":
        nut = 'fiber'

    return nut

def color_bars(df):
    colors = []
    cols = list(df.columns)
    for col in cols:
        val = float(df.loc[0,col])
        if val >= 100.:
            colors.append('rgb(255,0,0)')
        elif 100. > val >= 80.:
            colors.append('rgb(255,128,0)')
        elif 80. > val >= 60.:
            colors.append('rgb(0,255,0)')
        elif 60. > val >= 40.:
            colors.append('rgb(0,0,255)')
        else:
            colors.append('rgb(192,192,192)')
    return colors
