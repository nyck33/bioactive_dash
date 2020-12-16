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
########################################################################
def register_my_meals_callbacks(app):
    @app.callback(
        [Output('daterange-meals-table-out', 'children'),
        Output('daterange-rdi-chart', 'children')],
        Input('daterange-meals-btn', 'n_clicks'),
        [State('meal-dates-range', 'start_date'),
        State('meal-dates-range', 'end_date')]
    )
    def output_meals_table_period_rdi_chart(get_clicks,
                                            start_date,
                                            end_date):
        """
        table cols: meal_id, meal_type, meal_desc, timestamp
        make query with date range, make df, make table
        """
        if get_clicks is None or get_clicks<=0 or start_date is None or \
                end_date is None:
            return no_update

        user_id = ""
        if current_user.is_authenticated:
            user_id = current_user.id

        if start_date is not None:
            start_date_obj = date.fromisoformat(start_date)
            start_date_str = start_date_obj.strftime('%Y-%m-%d')
            #date object for comparisons
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

        if end_date is not None:
            end_date_obj= date.fromisoformat(end_date)
            end_date_str = end_date_obj.strftime('%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        meals_df = pd.DataFrame(columns=['meal_id', 'meal_type', 'meal_desc', 'timestamp'])

        conn = engine.connect()
        metadata = MetaData()
        user_meals = Table('user_meals', metadata, autoload=True, autoload_with=engine)
        stmt = select([user_meals])
        stmt = stmt.where(user_meals.columns.user_id == user_id and
                          start_date <= datetime.strptime(user_meals.columns.timestamp,
                                                          '%Y-%m-%d').date() <= end_date)
        results = conn.execute(stmt).fetchall()
        i=0
        for res in results:
            meals_df.loc[i, 'meal_id'] = res.meal_id
            meals_df.loc[i, 'meal_type'] = res.meal_type
            meals_df.loc[i, 'meal_desc'] = res.meal_desc
            meals_df.loc[i, 'timestamp'] = res.timestamp
            i+=1

        print(meals_df)
        # make the df_arr for all meals
        meals_df_arr = make_ingreds_df_for_meals(meals_df)

        #make nuts_totals_df
        nuts_totals_df = make_nuts_totals_df(meals_df_arr)

        # build rdi charts
        #todo: this assumes 3 meals per day everyday for period
        period_rdi_chart_ui = build_period_rdi_chart(nuts_totals_df,
                                                  start_date,
                                                  end_date)

        meals_ui = html.Div([
            DataTable(
                id='meals-table',
                data=meals_df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in meals_df.columns],
                row_deletable=True,
                row_selectable='multi',
                style_cell={'textAlign': 'left'},
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)'
                }],
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                }
            ),
            dcc.RadioItems(
                id="radio-data-display",
                options=[
                    {'label': 'Period Info', 'value': 'period-rdi'},
                    {'label': 'Meal and Ingredients Info', 'value': 'meal-rdi'},
                ],
                value='period-rdi'
            )
        ])

        return meals_ui, period_rdi_chart_ui

    #todo: make date range rdi chart:
    # first take meals_df and make an array of ingreds/meal df's
    # iterate the df array and fill a nuts total table
    # make charts based on percent of (rdi* num_days)
    def make_ingreds_df_for_meals(meals_df):
        """
        query user_ingreds for ingreds and fill df's to return
        meals_df_arr
        """
        conn = engine.connect()
        metadata = MetaData()
        user_meals = Table('user_ingreds', metadata, autoload=True, autoload_with=engine)
        stmt = select([user_meals])


        # make list of col
        meal_id_arr = list(meals_df['meal_id'])
        meals_df_arr = []
        for meal_id in meal_id_arr:
            # make df
            meal_df = pd.DataFrame(columns=['Ingredient', 'Amount', 'Units'])

            stmt = stmt.where(user_meals.columns.meal_id==meal_id)
            # get ingreds for each meal_id
            results = conn.execute(stmt).fetchall()
            i = 0
            for res in results:
                meal_df.loc[i,'Ingredient'] = res.ingred_name
                meal_df.loc[i, "Amount"] = res.ingred_amt
                meal_df.loc[i, "Units"] = res.ingred_units
                i+=1
            meals_df_arr.append(meal_df)

        return meals_df_arr

    def make_nuts_totals_df(meals_df_arr):
        """
        use function in notebook
        """
        # make df of nuts_totals
        nuts_totals_df = pd.concat({k: pd.Series(v) for k, v in
                                    nuts_totals_dict.items()}, axis=1)

        # set index to Name
        nuts_totals_df.set_index('Name', inplace=True, drop=False)

        for cumul_ingreds_df in meals_df_arr:
            for index, row in cumul_ingreds_df.iterrows():
                # get first ingred
                curr_ingred = row['Ingredient']
                curr_ingred_amt = row['Amount']  # amt of the ingred, not nutrient
                curr_ingred_units = row['Units']
                # get food_id of ingred and make df of all nutrients adjusted for amounts vs. conversion
                food_id = food_to_id_dict[curr_ingred]
                # get df of nuts for ingred
                ingred_nuts_df = make_nutrients_df(food_id)
                # get conversions df for ingred
                ingred_conversions_df = make_conversions_df(food_id)
                # get multiplier and measure num ie. 350 ml / 100 ml = 3.5
                curr_multiplier, measure_num = get_conversions_multiplier(ingred_conversions_df, curr_ingred_units)
                # updated nuts for ingred
                ingred_nuts_df = mult_nutrients_df(ingred_nuts_df, curr_multiplier, measure_num, curr_ingred_amt)

                # index into nutrients_totals_df and add value
                for idx, row in ingred_nuts_df.iterrows():
                    nut = row['Name']
                    val = float(row['Value'])  # add this to nuts_totals_df
                    units = row['Units']
                    # curr_totals_row = nuts_totals_df.loc[nuts_totals_df['Name']==nut]
                    # todo: make all fields strings
                    curr_total = nuts_totals_df.loc[nut, 'Value']
                    new_total = str(float(curr_total) + val)
                    nuts_totals_df.loc[nut, 'Value'] = new_total

        return nuts_totals_df

    def build_period_rdi_chart(nuts_totals_df, start_date, end_date):
        """
        use fn in rdi-charts-callbacks
        """
        #calc num days
        delta = end_date - start_date
        num_days = delta.days
        print(f'num days: {num_days}')
        usr_life_stg = ''
        usr_type = ''

        if current_user.is_authenticated:
            usr_life_stg = current_user.lifestage_grp
            usr_type = current_user.person_type

        # todo: index into each rdi_df and get col vals and multiply by num days
        rdi_e_df = rdi_elems_df.copy()
        rdi_v_df = rdi_vits_df.copy()
        rdi_mac_df = rdi_macros_df.copy()

        # https://stackoverflow.com/a/38543323/14767913
        # this only keeps the number cols and drops Life-Stage and others
        #rdi_e_df= rdi_e_df[rdi_e_df.select_dtypes(include=['number']).columns] * num_days
        #rdi_v_df= rdi_v_df[rdi_v_df.select_dtypes(include=['number']).columns] * num_days
        #rdi_mac_df= rdi_mac_df[rdi_mac_df.select_dtypes(include=['number']).columns] * num_days
        #todo: iterate df and multiply by num_days

        # df of nuts by category with field values as %
        elems_df = pd.DataFrame(columns=list(rdi_elems_dict.keys()))
        vits_df = pd.DataFrame(columns=list(rdi_vits_dict.keys()))
        macros_df = pd.DataFrame(columns=list(rdi_macros_dict.keys()))

        #fill row 0 of each nut_type df with percentages
        for idx, row in nuts_totals_df.iterrows():
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
                portion = rdi_e_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    # todo: could multiply num_days here
                    val = float(row[target_col].item()) * float(num_days)
                else:  # todo: this assumes when nan that any intake fulfills rda
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into elems_df and enter percent
                plot_cols = list(elems_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                elems_df.loc[0, target_col] = percent
            elif nut_type == 'vitamin':
                # get slice of df
                portion = rdi_v_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    val = float(row[target_col].item()) * float(num_days)
                else:
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into vits_df and enter percent
                plot_cols = list(vits_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                vits_df.loc[0, target_col] = percent
            elif nut_type == 'macronutrient':
                # get slice of df
                portion = rdi_mac_df.iloc[start_idx:end_idx, :].astype(str)
                row = portion[portion['Life-Stage Group'] == usr_life_stg]
                cols = list(row.columns)
                target_col = get_target_col(cnf_nut, cols)
                target_val = row[target_col].item()
                if target_val != 'nan' and target_val != 'ND':
                    val = float(row[target_col].item()) * float(num_days)
                else:
                    val = cnf_amt
                percent = ((cnf_amt * multiplier) / val) * 100.
                # index into macros_df and enter percent
                plot_cols = list(macros_df.columns)
                target_col = get_target_col(cnf_nut, plot_cols)
                macros_df.loc[0, target_col] = percent

        # make bar charts and html.Div containing them, return
        #style chart
        elem_colors = color_bars(elems_df)
        vits_colors = color_bars(vits_df)
        macros_colors = color_bars(macros_df)

        fig_elems = go.Figure(data=[go.Bar(
                    x=list(elems_df.columns),
                    y=list(elems_df.iloc[0]),
                    marker_color=elem_colors
        )])
        fig_elems.update_layout(title_text='elements for date range')
        fig_vits = go.Figure(data=[go.Bar(x=list(vits_df.columns),
                                     y=list(vits_df.iloc[0]),
                                     marker_color=vits_colors)])
        fig_vits.update_layout(title_text='vitamins for date range')
        fig_macros = go.Figure(data=[go.Bar(x=list(macros_df.columns),
                                       y=list(macros_df.iloc[0]),
                                       marker_color=macros_colors)])
        fig_macros.update_layout(title_text="macronutrients for date range")

        figs_div = html.Div([
            dcc.Graph(
                figure=fig_elems,
                id='period-elems-fig'
            ),
            dcc.Graph(
                figure=fig_vits,
                id='period-vits-fig'
            ),
            dcc.Graph(
                figure=fig_macros,
                id='period-macros-fig'
            )
        ])
        return figs_div


    #radio controls for layouts
    @app.callback(
        [Output('period-layout', 'style'),
         Output('per-selection-layout', 'style')],
        Input('radio-data-display', 'value')
    )
    def inject_layout(radio_val):
        if radio_val=='period-rdi':
            return {'display': 'block'}, {'display': 'none'}
        elif radio_val=='meal-rdi':
            return {'display': 'none'}, {'display': 'block'}

        return no_update, no_update
    '''
    @app.callback(
        [Output()]
    )
    '''