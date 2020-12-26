"""
import exacts, converts, not_match in rdi_callbacks
"""
# -*- coding: utf-8 -*-
"""
@author; Nobu Kim
"""
import pandas as pd


from dash_utils.Shiny_utils import (rdi_nutrients, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

from models import (
    CNFNutrientName
)

#rdi df_dict, #read from sql since csv's have alpha symbol
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
rdi_engine = create_engine("mysql+pymysql://root:tennis33@localhost/rdi_db?charset=utf8mb4")#, echo=True)

#print(rdi_engine.table_names())
# used in layout for datalist
food_to_id_dict, food_names_arr, food_ids_arr = make_food_to_id_dict()

# pure utils don't make stuff right after
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
        # #print(cnf_nut)
        for rdi_elem in rdi_units_dict.keys():
            # #print(rdi_elem)
            if cnf_nut in rdi_elem:
                cols.append(cnf_nut)

    return cols


#############################################################################
#make stuff right after function definition
# dict of cnf nutrient names: nutrient units
def make_cnf_data():
    nutrients = CNFNutrientName.objects
    cnf_nutr_dict = {}
    cnf_nutrient_names_all = []
    cnf_nutrient_units_all = []
    for n in nutrients:
        cnf_nutr_dict[str(n.name)] = str(n.unit)
        cnf_nutrient_names_all.append(str(n.name))
        cnf_nutrient_units_all.append(str(n.unit))

    assert len(cnf_nutrient_names_all) == len(cnf_nutrient_units_all)

    return cnf_nutr_dict, cnf_nutrient_names_all, cnf_nutrient_units_all


cnf_nutr_dict, cnf_nutrient_names_all, cnf_nutrient_units_all = make_cnf_data()

def make_nuts_totals_dict():
    num_values = len(cnf_nutrient_names_all)
    # make a base nutrients dataframe to cumulate into
    nuts_totals_dict = {
        "Name": cnf_nutrient_names_all,
        "Value": ["0" for i in range(num_values)],
        "Units": cnf_nutrient_units_all
    }
    return nuts_totals_dict

nuts_totals_dict = make_nuts_totals_dict()

def clean_cnf_arrs(cnf_units_arr):
    cnf_units_arr = [x.replace("\xb5g", "ug") for x in cnf_nutrient_units_all]
    cnf_units_arr = [x.replace(x, f'{x}/d') for x in cnf_units_arr]
    #print(len(cnf_units_arr))
    #print(cnf_units_arr)
    return cnf_units_arr

cnf_units_arr = clean_cnf_arrs(cnf_nutrient_units_all)
"""
# todo: make changes here to cnf_arr for the names of 
"""
def make_cnf_nuts_dict(nuts_totals_dict):
    #dict of {cnf_nut: cnf_units}
    cnf_arr = []
    names_arr = nuts_totals_dict['Name']
    for nut in names_arr:
        cnf_arr.append(nut.lower())
    ##print(len(cnf_arr))
    ##print(cnf_arr)
    cnf_nuts_dict = dict(zip(cnf_arr, cnf_units_arr))
    #for nut, units in cnf_nuts_dict.items():
    #for nut, units in cnf_nuts_dict.items():
     #   #print(f'{nut}:{units}')
    return cnf_nuts_dict

cnf_nuts_dict = make_cnf_nuts_dict(nuts_totals_dict)


def match_cnf_to_rdi_nut_names(cnf_nuts_dict):
    with_units_arr = []
    for nut, unit in cnf_nuts_dict.items():
        if nut=="fat (total lipids)":
            nut = 'fat'
        elif nut == "carbohydrate, total (by difference)":
            nut = 'carbohydrate'
        elif nut=="fibre, total dietary":
            nut = 'fiber'
        # todo: change this master list against which all incoming nuts_tables are
        # compared to deterimine nut_type: elements, vitamins, macros
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
        #elif nut == 'vitamin b12, added':
         #   nut = 'vitamin b12'
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

        with_units_arr.append(nut)

    #for k,v in cnf_nuts_dict.items():
        ##print(f'{k}:{v}')
    ##print(with_units_arr)
    ##print(nuts_totals_dict['Name'], len(nuts_totals_dict['Name']))
    cnf_nuts_dict = dict(zip(with_units_arr, cnf_units_arr))

    return cnf_nuts_dict

cnf_nuts_dict = match_cnf_to_rdi_nut_names(cnf_nuts_dict)


def make_df_dict():
    df_dict = {}
    for name in rdi_engine.table_names():
        '''
        if name != "macronutrients_dist_range" and name !=
        "elements_upper_rdi" and name != "vitamins_upper_rdi":
        '''
        sql = "SELECT * from " + name
        df = pd.read_sql_query(sql, rdi_engine)
        df_dict[name] = df
        #print(f'{name}\n{df}')

    return df_dict

df_dict = make_df_dict()
#print(len(df_dict))
# get lists of rdi_elements, rdi_vitamins, rdi_macros
elements_df = df_dict['elements_rdi']
vitamins_df = df_dict['vitamins_rdi']
macros_df = df_dict['macronutrients_rdi']
macro_distrange_df = df_dict['macronutrients_dist_range']

def clean_rdi_df(df):
    df_cols = [x.lower() for x in df.columns.tolist() if x != "Life-Stage Group"]
    nut_unit_dict = strip_units(df_cols)

    return df_cols, nut_unit_dict

rdi_elems_cols, rdi_elems_dict = clean_rdi_df(elements_df)

rdi_vits_cols, rdi_vits_dict = clean_rdi_df(vitamins_df)

rdi_macros_cols, rdi_macros_dict = clean_rdi_df(macros_df)

def make_rdi_nuts_arr(df_dict):
    # get all rdi nutrients
    rdi_nuts_arr = []
    for k, df in df_dict.items():
        for rdi_nut in df.columns.tolist():
            if rdi_nut != "Life-Stage Group":
                # #print(rdi_nut)
                if "Carbohydrates" in rdi_nut:
                    #print('here!')
                    rdi_nuts_arr.append("carbohydrate (g/d)")
                    continue
                if rdi_nut not in rdi_nuts_arr:
                    rdi_nuts_arr.append(rdi_nut.lower())

    return rdi_nuts_arr

rdi_nuts_arr = make_rdi_nuts_arr(df_dict)
#print(rdi_nuts_arr)

# take out extra word like total
def clean_rdi_nuts_arr(rdi_nuts_arr):
    rdi_arr = []
    for nut in rdi_nuts_arr:
        # take out total and fix fibre misspellling
        if 'total' in nut:  # total fiber, total fats
            new_nut = nut.replace('total', '').strip()
            rdi_arr.append(new_nut)
        else:
            rdi_arr.append(nut)

    return rdi_arr

rdi_arr = clean_rdi_nuts_arr(rdi_nuts_arr)

#print(rdi_arr)

# strip the units out
# dict {nut: units}
def make_rdi_units_dict():
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

    return rdi_units_dict

rdi_units_dict = make_rdi_units_dict()

#for nut, units in rdi_units_dict.items():
    #print(f'{nut}:{units}')

'''
#compare incoming cnf data with rdi benchmarks
compare the keys and include the matches in comparisons (missing sci-name nuts)
then compare the units to see which need conversions
exact_matches=[[{cnf:units},{rdi:units}]], convers_matches = [[{},{}]]
no_match= [cnf no rdi equivalent]
rdi_unused = []
'''
def search_cnf_nuts_in_rdi_nuts(cnf_nuts_dict, rdi_units_dict):

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

    return exacts, converts, not_match, rdi_unused

exacts, converts, not_match, rdi_unused = search_cnf_nuts_in_rdi_nuts(cnf_nuts_dict,
                                                                      rdi_units_dict)

#print(len(exacts), exacts)
#print(f'\n\nconvert: {len(converts)}\n{converts}')
#print(f'\n\nno match:{len(not_match)}\n{not_match}')
#todo: only doing exacts but what about converts?
def make_cnf_elems_vits_macros_dicts(exacts):
    cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts = [], [], []

    for match in exacts:
        cnf = match[0]

        cnf_nut = list(cnf.keys())[0]
        cnf_units = list(cnf.values())[0]
        # #print(cnf_nut, cnf_units)
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

    return cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts

cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts = make_cnf_elems_vits_macros_dicts(exacts)

#print(len(cnf_elems_dicts), len(cnf_vits_dicts), len(cnf_macros_dicts))
#print(cnf_elems_dicts, cnf_vits_dicts, cnf_macros_dicts)

def get_calories_dfs():
    """
    get calories tables for males and females
    """
    males_table_name = 'males_calories'

    sql = "SELECT * from " + males_table_name

    males_df = pd.read_sql_query(sql, rdi_engine)

    females_table = 'females_calories'

    sql2 = "SELECT * from " + females_table

    females_df = pd.read_sql_query(sql2, rdi_engine)

    return males_df, females_df

males_df, females_df = get_calories_dfs()

def get_calories_per_day(person_type, age, active_lvl):
    """
    index into males_df and females_df
    cols: age, sedentary, moderately_active, active
    param: age is a decimal so 0.5 for 6 mo's
    Return: calories per day as int
    """
    # todo: change this to handle baby ages properly
    if not age.isdigit():
        age = 2
    else:
        # change age to int
        age = int(age)

    # change pregnant or lactating to female:
    if 'preg' in person_type or 'lact' in person_type:
        person_type = 'female'

    df = None
    if person_type=='male':
        df = males_df
    else:
        df = females_df

    val = ""

    if 2 <= age <= 18:
        idx = df.index[df['age'] == str(age)][0]
        val = df.loc[idx, active_lvl]
    elif age < 2.: #todo: calc val here
        row = df[df['age'] == '2']
    elif age >= 76:
        val = df[active_lvl].iloc[-1]
    else:
        for idx, row in df.iterrows():
            if "-" in row['age']:
                age_grp = row['age'].split('-')
                age_grp = [int(x) for x in age_grp]
                low = age_grp[0]
                high = age_grp[1]
                if low <= age <= high:
                    #the_idx = idx
                    val = df.loc[idx, active_lvl]
                    break

    val = int(val.replace(",", ""))

    return val