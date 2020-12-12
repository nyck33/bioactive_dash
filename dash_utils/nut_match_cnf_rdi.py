"""
import exacts, converts, not_match in rdi_callbacks
"""
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

from dash_utils.Shiny_utils import (rdi_nutrients, rdi_modelnames_arr, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)


# function to take out units
def strip_units(nuts_arr):
    nuts_units_dict = {}
    for nut in nuts_arr:
        # take out units
        if '(g/d)' in nut:
            curr_units = 'g/d'
            new_nut = nut.replace('(g/d)', '').strip()
            nuts_units_dict[new_nut] = curr_units
        elif '(mg/d)' in nut:
            curr_units = 'mg/d'
            new_nut = nut.replace('(mg/d)', '').strip()
            nuts_units_dict[new_nut] = curr_units
        elif '(ug/d)' in nut:
            curr_units = 'ug/d'
            new_nut = nut.replace('(ug/d)', '').strip()
            nuts_units_dict[new_nut] = curr_units
        elif '(l/d)' in nut:
            curr_units = 'l/d'
            new_nut = nut.replace('(l/d)', '').strip()
            nuts_units_dict[new_nut] = curr_units
        else:  # carotenoid -> alpha-carotene, beta-carotene?
            new_nut = nut
            nuts_units_dict[new_nut] = ''

    return nuts_units_dict

# iterate ingreds_df
def get_df_cols(df_name):
    cols = []
    for cnf_nut in cnf_nuts_dict.keys():
        # print(cnf_nut)
        for rdi_elem in rdi_units_dict.keys():
            # print(rdi_elem)
            if cnf_nut in rdi_elem:
                cols.append(cnf_nut)

    return cols

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
cnf_units_arr = [x.replace("\xb5g", "ug") for x in cnf_nutrient_units_all]
cnf_units_arr = [x.replace(x, f'{x}/d') for x in cnf_units_arr]
print(len(cnf_units_arr))
print(cnf_units_arr)

#dict of {cnf_nut: cnf_units}
cnf_arr = []
for nut in nuts_totals_dict['Name']:
    cnf_arr.append(nut.lower())
#print(len(cnf_arr))
#print(cnf_arr)
cnf_nuts_dict = dict(zip(cnf_arr, cnf_units_arr))
#for nut, units in cnf_nuts_dict.items():
#for nut, units in cnf_nuts_dict.items():
 #   print(f'{nut}:{units}')

with_units_arr = []
for nut, unit in cnf_nuts_dict.items():
    if nut=="fat (total lipids)":
        nut = 'fat'
    elif nut == "carbohydrate, total (by difference)":
        nut = 'carbohydrate'
    elif nut=="fibre, total dietary":
        nut = 'fiber'
    with_units_arr.append(nut)

#for k,v in cnf_nuts_dict.items():
    #print(f'{k}:{v}')
#print(with_units_arr)
#print(nuts_totals_dict['Name'], len(nuts_totals_dict['Name']))
cnf_nuts_dict = dict(zip(with_units_arr, cnf_units_arr))

for nut, units in cnf_nuts_dict.items():
    print(f'{nut}:{units}')

#rdi df_dict, #read from sql since csv's have alpha symbol
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql
rdi_engine = create_engine("mysql+pymysql://root:tennis33@localhost/rdi_db?charset=utf8mb4")#, echo=True)

print(rdi_engine.table_names())

import pandas as pd
df_dict = {}
for name in rdi_engine.table_names():
    if name != "macronutrients_dist_range" and name !=\
    "elements_upper_rdi" and name != "vitamins_upper_rdi":
        sql = "SELECT * from " + name
        df = pd.read_sql_query(sql, rdi_engine)
        df_dict[name] = df
        print(f'{name}\n{df}')

print(len(df_dict))

# get lists of rdi_elements, rdi_vitamins, rdi_macros
elements_df = df_dict['elements_rdi']
vitamins_df = df_dict['vitamins_rdi']
macros_df = df_dict['macronutrients_rdi']

rdi_elements = [x.lower() for x in elements_df.columns.tolist() if x != "Life-Stage Group"]
rdi_elems_dict = strip_units(rdi_elements)
print(len(rdi_elements))
print(len(rdi_elems_dict))
for nut, units in rdi_elems_dict.items():
    print(f'{nut}:{units}')

rdi_vitamins = [x.lower() for x in vitamins_df.columns.tolist() if x != "Life-Stage Group"]
rdi_vits_dict = strip_units(rdi_vitamins)
print(len(rdi_vitamins))
print(len(rdi_vits_dict))
for nut, units in rdi_vits_dict.items():
    print(f'{nut}:{units}')

rdi_macros = [x.lower() for x in macros_df.columns.tolist() if x != "Life-Stage Group"]
rdi_macros_dict = strip_units(rdi_macros)
print(len(rdi_macros))
print(len(rdi_macros_dict))
for nut, units in rdi_macros_dict.items():
    print(f'{nut}:{units}')

# get all rdi nutrients
rdi_nuts_arr = []
for k, df in df_dict.items():
    for rdi_nut in df.columns.tolist():
        if rdi_nut != "Life-Stage Group":
            # print(rdi_nut)
            if "Carbohydrates" in rdi_nut:
                print('here!')
                rdi_nuts_arr.append("carbohydrate (g/d)")
                continue
            if rdi_nut not in rdi_nuts_arr:
                rdi_nuts_arr.append(rdi_nut.lower())

print(rdi_nuts_arr)

# take out extra word like total
rdi_arr = []
for nut in rdi_nuts_arr:
    # take out total and fix fibre misspellling
    if 'total' in nut:  # total fiber, total fats
        new_nut = nut.replace('total', '').strip()
        rdi_arr.append(new_nut)
    else:
        rdi_arr.append(nut)

print(rdi_arr)

# strip the units out
# dict {nut: units}
rdi_units_dict = {}
for nut in rdi_arr:
    # take out units
    if '(g/d)' in nut:
        curr_units = 'g/d'
        new_nut = nut.replace('(g/d)', '').strip()
        rdi_units_dict[new_nut] = curr_units
    elif '(mg/d)' in nut:
        curr_units = 'mg/d'
        new_nut = nut.replace('(mg/d)', '').strip()
        rdi_units_dict[new_nut] = curr_units
    elif '(ug/d)' in nut:
        curr_units = 'ug/d'
        new_nut = nut.replace('(ug/d)', '').strip()
        rdi_units_dict[new_nut] = curr_units
    elif '(l/d)' in nut:
        curr_units = 'l/d'
        new_nut = nut.replace('(l/d)', '').strip()
        rdi_units_dict[new_nut] = curr_units
    else: # carotenoid -> alpha-carotene, beta-carotene?
        new_nut = nut
        rdi_units_dict[new_nut] = ''

for nut, units in rdi_units_dict.items():
    print(f'{nut}:{units}')

'''
#compare incoming cnf data with rdi benchmarks
compare the keys and include the matches in comparisons (missing sci-name nuts)
then compare the units to see which need conversions
exact_matches=[[{cnf:units},{rdi:units}]], convers_matches = [[{},{}]]
no_match= [cnf no rdi equivalent]
rdi_unused = []
'''
exacts = []
converts = []
not_match = []
rdi_unused = []
exact = False
convert = False
for nut, units in cnf_nuts_dict.items():
    for rdi_nut, rdi_units in rdi_units_dict.items():
        if nut in rdi_nut and units in rdi_units:
            exact = True
            exacts.append([{nut: units}, {rdi_nut: rdi_units}])

        elif nut in rdi_nut and units not in rdi_units:
            convert = True
            converts.append([{nut: units}, {rdi_nut: rdi_units}])

    if exact == False and convert == False:
        not_match.append({nut: units})
    exact = False
    convert = False

print(len(exacts), exacts)
print(f'\n\nconvert: {len(converts)}\n{converts}')
print(f'\n\nno match:{len(not_match)}\n{not_match}')

cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts = [], [], []

for match in exacts:
    cnf = match[0]

    cnf_nut = list(cnf.keys())[0]
    cnf_units = list(cnf.values())[0]
    # print(cnf_nut, cnf_units)
    rdi = match[1]
    rdi_nut = list(rdi.keys())[0]
    rdi_units = list(rdi.values())[0]
    for rdi_n, _ in rdi_elems_dict.items():
        if cnf_nut in rdi_n:
            cnf_elems_dicts.append([{cnf_nut: cnf_units}, {rdi_nut: rdi_units}])
            continue
    for rdi_n, _ in rdi_vits_dict.items():
        if cnf_nut in rdi_n:
            cnf_vits_dicts.append([{cnf_nut: cnf_units}, {rdi_nut: rdi_units}])
            continue
    for rdi_n, _ in rdi_macros_dict.items():
        if cnf_nut in rdi_n:
            cnf_macros_dicts.append([{cnf_nut: cnf_units}, {rdi_nut: rdi_units}])
            continue

print(len(cnf_elems_dicts), len(cnf_vits_dicts), len(cnf_macros_dicts))
print(cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts)
