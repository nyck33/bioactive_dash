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
import plotly.graph_objects as go
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
#utilities import
from dash_utils.make_meal_utils import (get_target_col, get_lifestage_idxs,
                                        find_type, preprocess_cnf_nuts,
                                        color_bars)
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
        #print(ingred_df)
        # df of nuts by category with field values as %
        elems_df = pd.DataFrame(columns=list(rdi_elems_dict.keys()))
        vits_df = pd.DataFrame(columns=list(rdi_vits_dict.keys()))
        macros_df = pd.DataFrame(columns=list(rdi_macros_dict.keys()))

        #calculate percentages
        # get row in each df elem_rdi, vit_rdi, macros_rdi
        for idx, row in ingred_df.iterrows():
            #todo: need to process and take out brackets, extra words
            cnf_nut = row['Name'].lower()
            cnf_nut = preprocess_cnf_nuts(cnf_nut)
            cnf_amt = float(row['Value'])
            # todo: take out micro symbol from units but not used as units
            # taken from dicts_arrs in def find_type
            cnf_units = row['Units']
            if '\xb5g' in cnf_units:
                cnf_units = cnf_units.replace("\xb5g", "ug")
            nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_elems_dicts)
            if nut_type=="":
                nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_vits_dicts)
            if nut_type=="":
                nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_macros_dicts)

            # get start and exclusive end idx of rdi_df
            start_idx, end_idx = get_lifestage_idxs(usr_type)
            if nut_type =='element':
                # get slice of df
                portion = rdi_elems_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    val = float(row[target_col].item())
                else: #todo: this assumes when nan that any intake fulfills rda
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into elems_df and enter percent
                plot_cols = list(elems_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                elems_df.loc[0, target_col] = percent
            elif nut_type == 'vitamin':
                # get slice of df
                portion = rdi_vits_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    val = float(row[target_col].item())
                else:
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into vits_df and enter percent
                plot_cols = list(vits_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                vits_df.loc[0, target_col] = percent
            elif nut_type == 'macronutrient':
                # get slice of df
                portion = rdi_macros_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group']==usr_life_stg]
                cols= list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val!= 'nan' and target_val!='ND':
                    val = float(row[target_col].item())
                else:
                    val=cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                #index into macros_df and enter percent
                plot_cols = list(macros_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                macros_df.loc[0, target_col] = percent

        #style chart
        elem_colors = color_bars(elems_df)
        vits_colors = color_bars(vits_df)
        macros_colors = color_bars(macros_df)

        fig_elems = go.Figure(data=[go.Bar(
                    x=list(elems_df.columns),
                    y=list(elems_df.iloc[0]),
                    marker_color=elem_colors
        )])
        fig_elems.update_layout(title_text='elements for ingredient')
        fig_vits = go.Figure(data=[go.Bar(x=list(vits_df.columns),
                                     y=list(vits_df.iloc[0]),
                                     marker_color=vits_colors)])
        fig_vits.update_layout(title_text='vitamins for ingredient')
        fig_macros = go.Figure(data=[go.Bar(x=list(macros_df.columns),
                                       y=list(macros_df.iloc[0]),
                                       marker_color=macros_colors)])
        fig_macros.update_layout(title_text="macronutrients for ingredient")
        return fig_elems, fig_vits, fig_macros

    def check_macros_dist_range():
        """
        9 calories per fat gram so multiply and divid by KCal
        to get percentage.  Fiber for infants is also ND.
        Then map against upper range of macro-dist-range which is missing.

        """
        pass
    @app.callback(
        [Output('cnf-vs-rdi-totals-elements', 'figure'),
         Output('cnf-vs-rdi-totals-vitamins', 'figure'),
         Output('cnf-vs-rdi-totals-macro', 'figure')],
        [Input('hidden-total-nutrients-df', 'data')]
    )
    def update_total_nuts_charts(total_nuts_json):
        usr_life_stg = ''
        usr_type = ''
        if current_user.is_authenticated:
            usr_life_stg = current_user.lifestage_grp
            usr_type = current_user.person_type

        if total_nuts_json is None:
            return no_update, no_update, no_update

        # Name Value Units
        total_nuts_df = pd.read_json(total_nuts_json, orient='split')
        #print(total_nuts_df)
        # df of nuts by category with field values as %
        elems_df = pd.DataFrame(columns=list(rdi_elems_dict.keys()))
        vits_df = pd.DataFrame(columns=list(rdi_vits_dict.keys()))
        macros_df = pd.DataFrame(columns=list(rdi_macros_dict.keys()))

        # calculate percentages
        # get row in each df elem_rdi, vit_rdi, macros_rdi
        for idx, row in total_nuts_df.iterrows():
            # todo: need to process and take out brackets, extra words
            cnf_nut = row['Name'].lower()
            cnf_nut = preprocess_cnf_nuts(cnf_nut)
            cnf_amt = float(row['Value'])
            # todo: take out micro symbol from units but not used as units
            # taken from dicts_arrs in def find_type
            cnf_units = row['Units']
            if '\xb5g' in cnf_units:
                cnf_units = cnf_units.replace("\xb5g", "ug")
            nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_elems_dicts)
            if nut_type == "":
                nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_vits_dicts)
            if nut_type == "":
                nut_type, rdi_nut, multiplier = find_type(cnf_nut, cnf_macros_dicts)

            # get start and exclusive end idx of rdi_df
            start_idx, end_idx = get_lifestage_idxs(usr_type)
            if nut_type == 'element':
                # get slice of df
                portion = rdi_elems_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    val = float(row[target_col].item())
                else:  # todo: this assumes when nan that any intake fulfills rda
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into elems_df and enter percent
                plot_cols = list(elems_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                elems_df.loc[0, target_col] = percent
            elif nut_type == 'vitamin':
                # get slice of df
                portion = rdi_vits_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    val = float(row[target_col].item())
                else:
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into vits_df and enter percent
                plot_cols = list(vits_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                vits_df.loc[0, target_col] = percent
            elif nut_type == 'macronutrient':
                # get slice of df
                portion = rdi_macros_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    val = float(row[target_col].item())
                else:
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into macros_df and enter percent
                plot_cols = list(macros_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                macros_df.loc[0, target_col] = percent

        #style chart
        elem_colors = color_bars(elems_df)
        vits_colors = color_bars(vits_df)
        macros_colors = color_bars(macros_df)

        fig_elems = go.Figure(data=[go.Bar(
                    x=list(elems_df.columns),
                    y=list(elems_df.iloc[0]),
                    marker_color=elem_colors
        )])
        fig_elems.update_layout(title_text='elements for recipe')
        fig_vits = go.Figure(data=[go.Bar(x=list(vits_df.columns),
                                     y=list(vits_df.iloc[0]),
                                     marker_color=vits_colors)])
        fig_vits.update_layout(title_text='vitamins for recipe')
        fig_macros = go.Figure(data=[go.Bar(x=list(macros_df.columns),
                                       y=list(macros_df.iloc[0]),
                                       marker_color=macros_colors)])
        fig_macros.update_layout(title_text="macronutrients for recipe")

        return fig_elems, fig_vits, fig_macros
