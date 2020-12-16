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

from dash_utils.my_meals_utils import (make_ingreds_df_for_meals,
                                       make_nuts_totals_df,
                                       build_period_rdi_chart,
                                       make_datatable)

from dash_utils.bonAPI import (get_bon_alt_ingreds,
                                make_alt_ingreds_ui,
                               make_save_alts_ui)

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
                                                  end_date,
                                                charts_label=' for date range',
                                                elem_fig_id='daterange-elems-fig',
                                                vits_fig_id='daterange-vits-fig',
                                                macros_fig_id='daterange-macros-fig')

        meals_table = make_datatable('meals-table', meals_df, 'single')

        meals_ui = html.Div([
            meals_table,
            dcc.RadioItems(
                id="radio-data-display",
                options=[
                    {'label': 'Period Info', 'value': 'period-rdi'},
                    {'label': 'Meal and Ingredients Info', 'value': 'meal-rdi'},
                    {'label': 'Ingredient Alternatives', 'value': 'alt-ingreds'}
                ],
                value='period-rdi'
            )
        ])

        return meals_ui, period_rdi_chart_ui

    #radio controls for layouts
    @app.callback(
        [Output('period-layout', 'style'),
         Output('per-selection-layout', 'style'),
         Output('alt-ingreds-layout', 'style')],
        Input('radio-data-display', 'value')
    )
    def inject_layout(radio_val):
        if radio_val=='period-rdi':
            return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
        elif radio_val=='meal-rdi':
            return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
        elif radio_val =='alt-ingreds':
            return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
        return no_update, no_update, no_update

    #output ingreds for selected rows from meals table
    """
    cols: meal_id, timestamp, ingred_name, ingred_amt, ingred_units
    """
    @app.callback(
        [Output('selections-rdi-chart-out', 'children'),
         Output('selections-ingreds-table-out', 'children')],
        [Input('meals-table', 'data'),
        Input('meals-table', 'selected_rows')]
    )
    def output_meals_selections_table_chart(rows, selected_row):
        if selected_row is None or selected_row == []:
            return no_update, no_update

        # from this df, iterrate rows to get ingredients,
        # make ingredients_df and total_nuts
        selected_row = [rows[i] for i in selected_row]
        selected_meal_df = pd.DataFrame(selected_row)

        # make ingreds_df (cumulative for selected meal), returns df_arr
        ingreds_df_arr = make_ingreds_df_for_meals(selected_meal_df)

        ingreds_df = ingreds_df_arr[0]

        ingreds_table = make_datatable('meal-ingreds-table', ingreds_df,
                                       'single')

        ingreds_tbl_ui = make_alt_ingreds_ui(ingreds_table)

        nuts_totals_df = make_nuts_totals_df(ingreds_df_arr)

        rdi_figs_div = build_period_rdi_chart(nuts_totals_df,
                                              charts_label=' for meal',
                                              elem_fig_id='meal-elems-fig',
                                              vits_fig_id='meal-vits-fig',
                                              macros_fig_id='meal-macros-fig')

        return rdi_figs_div, ingreds_tbl_ui

    """
    show rdi for selected ingredient and search alternative, show,
    table of alternatives that can be selected to show rdi for each
    
    """
    @app.callback(
        Output('ingred-rdi-chart-out', 'children'),
        [Input('meal-ingreds-table', 'data'),
        Input('meal-ingreds-table', 'selected_rows')]
    )
    def output_ingreds_table_chart(rows, selected_row):
        if selected_row is None or selected_row == []:
            return no_update

        selected_row = [rows[i] for i in selected_row]
        # single ingred df
        selected_ingred_df = pd.DataFrame(selected_row)

        # get the ingredient name
        #ingred_name = selected_ingred_df.loc[0, 'Ingredient']

        # find alternatives
        ingreds_df_arr = [selected_ingred_df]
        #for single ingredient
        nuts_totals_df = make_nuts_totals_df(ingreds_df_arr)

        rdi_figs_div = build_period_rdi_chart(nuts_totals_df,
                                              charts_label=' for ingredients',
                                              elem_fig_id='ingreds-elems-fig',
                                              vits_fig_id='ingreds-vits-fig',
                                              macros_fig_id='ingreds-macros-fig')

        return rdi_figs_div
    """
    can't output rdi-chart-alt-ingred without searching database
    for matches, ex. coconut-based mozzarella == ?
    """
    @app.callback(
        [Output('alt-ingreds-table-out', 'children'),
        Output('rdi-chart-alt-ingred-out', 'children')],
        Input('search-alt-btn', 'n_clicks'),
        [State('alt-ingreds-text', 'value'),
         State('allergies-dropdown', 'value'), #str
         State('diet-dropdown', 'value')]
    )
    def find_alt_ingreds(n_clicks, foods, allergies, diet):
        if n_clicks is None or n_clicks <= 0:
            return no_update, no_update

        #todo foods comes in as comma-separated string, need underscores
        #strip whitespace
        foods_arr = foods.split(',')
        print(foods_arr)
        # new arr
        cleaned_foods = []
        for food in foods_arr:
            curr_food_arr = food.split()
            if len(curr_food_arr) > 1: #if ie. chicken breast -> chicken_breast
                curr_food = '_'.join(x for x in curr_food_arr)
                cleaned_foods.append(curr_food)
            else:
                cleaned_foods.append(food)
        print(cleaned_foods)
        foods_str = ",".join(x for x in cleaned_foods)
        #allergies is a list of strings so join and need allergies=
        allergies_str = ""
        if isinstance(allergies, list):
            allergies_str = ",".join(x for x in allergies)
        else:
            allergies_str = allergies
        # allergies=
        allergies_str = "allergies=" + allergies_str
        #diet=
        diet_str = "diet=" + diet

        res_json = get_bon_alt_ingreds(foods_str, allergies_str, diet_str)
        print(res_json)
        res_dict = json.loads(res_json)
        print(res_dict)
        # get arr
        updated_ingreds = res_dict['response']['updated_ingredients']
        # convert
        updated_ingreds_str = ','.join(x for x in updated_ingreds)

        save_alts_ui = make_save_alts_ui(updated_ingreds_str)

        return save_alts_ui, 'coming soon' #rdi chart for alts not ready
