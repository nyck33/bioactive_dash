"""
# -*- coding: utf-8 -*-
"""
#@author; Nobu Kim

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
#todo: move to app
#connect to Mongo
#connect('cnf')
from server import db_mongo

from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)
from models.model_nutrients import (
    ElementsRDI, VitaminsRDI, ElementsUpperRDI,
    VitaminsUpperRDI, MacronutrientsDistRange
)
from models.model_infantsRDI import (
    InfantsElementsRDI, InfantsVitaminsRDI, InfantsMacroRDI, InfantsElementsUpperRDI, \
    InfantsVitaminsUpperRDI
)
from models.model_childrenRDI import (
    ChildrenElementsRDI, ChildrenVitaminsRDI, ChildrenMacroRDI, ChildrenElementsUpperRDI, \
    ChildrenVitaminsUpperRDI
)
from models.model_malesRDI import (
    MalesElementsRDI, MalesVitaminsRDI, MalesMacroRDI, MalesElementsUpperRDI, MalesVitaminsUpperRDI
)
from models.model_femalesRDI import (
    FemalesElementsRDI, FemalesVitaminsRDI, FemalesMacroRDI, FemalesElementsUpperRDI, \
    FemalesVitaminsUpperRDI
)
from models.model_pregnancyRDI import (
    PregnancyElementsRDI, PregnancyVitaminsRDI, PregnancyMacroRDI, PregnancyElementsUpperRDI, \
    PregnancyVitaminsUpperRDI
)
from models.model_lactationRDI import (
    LactationElementsRDI, LactationVitaminsRDI, LactationMacroRDI, LactationElementsUpperRDI, \
    LactationVitaminsUpperRDI
)

# import the rdi csv table names and filenames arrs
from dash_utils.Dash_App_utils import (table_names_arr, csv_names_arr, make_dataframes,
                                            make_table, make_figure)

from dash_utils.Shiny_utils import (rdi_nutrients, rdi_modelnames_arr, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

#from .layouts.Shiny_hidden_layouts import (cnf_layout, cnf_totals_layout)
from .layouts.make_meal_layout import controls_layout, cnf_layout, cnf_totals_layout
from .callbacks.make_meal_callbacks import register_make_meal_callbacks
#for Flask Login
import random
from flask_login import current_user
import time
from functools import wraps

from server import app

login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

location = dcc.Location(id='make-meal-url',refresh=True)


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


def layout():
    full_layout = html.Div([controls_layout, cnf_layout, cnf_totals_layout])

    return full_layout


register_make_meal_callbacks(app)

###############################################################################################################
# updates visibility of containers
@app.callback(
    [Output('cnf-layout', 'style'),
     Output('cnf-totals-layout', 'style')],
    [Input('radio-display-type', 'value')]
)
def inject_layout(radio_val):
    if radio_val == 'cnf-table':
        return {'display': 'block'}, {'display': 'none'}
    elif radio_val == 'cnf-totals-table':
        return {'display': 'none'}, {'display': 'block'}
    return no_update, no_update

@app.callback(
    [Output('chosen-food', 'children'),
     Output('units-dropdown', 'options')],
    Input('search-ingredient', 'value')
)
def update_dropdown(ingredient):
    if ingredient == None or ingredient == "":
        return no_update, no_update
    food_name = html.H3(f"You chose: {ingredient}")
    # get food_id
    food_id = food_to_id_dict[ingredient]
    # get units, todo: why does it want a list?
    measure_names = get_unit_names(food_id)  # [0]
    # make dict to return options for dropdown
    foodnameDict = {ingredient: measure_names}

    return food_name, [{'label': unit, 'value': unit} for unit in foodnameDict[ingredient]]

# call back to show conversions table, nutrients table and food group/src table
# for currently selected ingredient
# todo: add another column in nutrients table for all ingredients

@app.callback(
    [Output('hidden-conversions-df', 'children'),
     Output('hidden-nutrients-df', 'data'),
     Output('table-foodgroup-source', 'data'),
     Output('table-foodgroup-source', 'columns'),
     Output('conversions-table', 'data'),
     Output('conversions-table', 'columns'),
     Output('nutrients-table', 'data'),
     Output('nutrients-table', 'columns'),
     Output('err-nutrients-table', 'children'),
     Output('ctx-msg', 'children')],
    [Input('search-ingredient-btn', 'n_clicks'),
     Input('update-nut-table-btn', 'n_clicks')],
    [State('hidden-conversions-df', 'children'),
     State('hidden-nutrients-df', 'data'),
     State('search-ingredient', 'value'),
     State("numerical-amount", "value"),
     State('units-dropdown', 'value')]
)
def show_update_tables(ingredient_clicks, add_clicks, conversions_json, nutrients_json,
                       ingredient, amt, units):
    '''
    return top table, conversions table, nutrients table, yield table,
    refuse table
    #todo: get state of cumul ingredients table with name, amount, units
    #hide in hidden div for sue with rdi, add column to table when there are
    #other cumul ingredients
    '''
    # if ingredient_clicks <=0 and add_clicks <= 0:
    # return no_update, no_update
    ctx = callback_context
    # get id of trigger
    trigger = ctx.triggered[0]['prop_id'].split(".")[0]
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    food_id = -1
    if ingredient is not None:
        food_id = food_to_id_dict[ingredient]

    if trigger == 'search-ingredient-btn' and ingredient_clicks > 0:
        foodgroup_df = make_foodgroup_df(food_id)
        foodgroup_cols = [{"name": i, "id": i} for i in foodgroup_df.columns]
        foodgroup_data = foodgroup_df.to_dict('records')

        conversions_df = make_conversions_df(food_id)
        conversions_cols = [{"name": i, "id": i} for i in conversions_df.columns]
        conversions_data = conversions_df.to_dict('records')
        conversions_json = conversions_df.to_json(date_format='iso', orient='split')

        nutrients_df = make_nutrients_df(food_id)
        nutrients_cols = [{"name": i, "id": i} for i in nutrients_df.columns]
        nutrients_data = nutrients_df.to_dict('records')
        # change to json format for intermediate value
        nutrients_json = nutrients_df.to_json(date_format='iso', orient='split')

        return conversions_json, nutrients_json, foodgroup_data, foodgroup_cols, conversions_data, \
               conversions_cols, nutrients_data, nutrients_cols, 'first output', ctx_msg

    elif trigger == 'update-nut-table-btn' and add_clicks > 0:
        # must use base table for math
        # nutrients_df = make_nutrients_df(food_id)
        nutrients_df = pd.read_json(nutrients_json, orient='split')
        conversions_df = pd.read_json(conversions_json, orient='split')
        curr_multiplier, measure_num = get_conversions_multiplier(conversions_df, units)
        # divide amount/measure_num
        nutrients_df = mult_nutrients_df(nutrients_df, curr_multiplier, measure_num, amt)

        nutrients_cols = [{"name": i, "id": i} for i in nutrients_df.columns]
        nutrients_data = nutrients_df.to_dict('records')

        # update the hidden nutrients-df for appending in add-ingred function
        nutrients_json = nutrients_df.to_json(date_format='iso', orient='split')

        return no_update, nutrients_json, no_update, no_update, no_update, no_update, nutrients_data, nutrients_cols, \
               'update nutrients table', ctx_msg

    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
           'none updated', ctx_msg

# chained callback to update the total-nutrients-hidden-df and output
# to total-nutrients-datatable
@app.callback(
    [Output('hidden-total-nutrients-df', 'data'),
     Output('cnf-totals-table', 'data'),
     Output('cnf-totals-table', 'columns')],
    [Input('add-ingredient', 'n_clicks')],
    [State('hidden-nutrients-df', 'data'),
     State('hidden-total-nutrients-df', 'data')]
)
def update_total_nutrients_df(num_clicks, nutrients_json, total_nutrients_json):
    """
    Total-nutrients-df has cols with no value when that row's nutrient is non-existent in
    all added ingredients
    Step:
    #iterate rows of cumul_ingreds: Ingredient, Amount, Units to get name, amt, units
    # get food id from ingred to make df's of conversions and nutrients
    # then call conversions_multiplier and mult_nutrients_table to get multiplied_df
    """
    if num_clicks <= 0:
        return no_update, no_update, no_update

    nutrients_totals_df = None
    if total_nutrients_json is None:
        nutrients_totals_df = pd.concat({k: pd.Series(v) for k, v in
                                         nutrients_totals_dict.items()}, axis=1)
    else:
        # add to this
        nutrients_totals_df = pd.read_json(total_nutrients_json, orient='split')

    if nutrients_json is None:
        return no_update, no_update, no_update

    nutrients_df = pd.read_json(nutrients_json, orient='split')

    # total_nutrients_df = pd.read_json(total_nutrients_json, orient='split')
    nutrients_totals_df.set_index('Name', inplace=True, drop=False)

    for index, row in nutrients_df.iterrows():
        curr_ingred = row['Name']
        curr_ingred_amt = row['Value']
        curr_ingred_units = row['Units']
        # index into nutrients_totals_df and add value
        curr_total_nutrient = float(nutrients_totals_df.loc[curr_ingred, 'Value'])
        new_total_nutrient = curr_total_nutrient + curr_ingred_amt
        nutrients_totals_df.loc[[curr_ingred], ['Value']] = new_total_nutrient

    nutrients_totals_json = nutrients_totals_df.to_json(date_format='iso', orient='split')

    # return json, dict and cols
    total_nutrients_json = nutrients_totals_df.to_json(date_format='iso', orient='split')
    cnf_totals_table_data = nutrients_totals_df.to_dict('records')
    cnf_totals_table_cols = [{'name': i, "id": i} for i in nutrients_totals_df.columns]

    return total_nutrients_json, cnf_totals_table_data, cnf_totals_table_cols

# for display at the top
@app.callback(
    [Output('hidden-cumul-ingreds-df', 'children'),
     Output('cumul-ingreds-table', 'data'),
     Output('cumul-ingreds-table', 'columns')],
    [Input('add-ingredient', 'n_clicks'),
     Input('remove-ingredient', 'n_clicks')],
    [State('hidden-cumul-ingreds-df', 'children'),
     State('search-ingredient', 'value'),
     State("numerical-amount", "value"),
     State('units-dropdown', 'value'),
     State('hidden-nutrients-df', 'data')]
)
def update_cum_ingredients_table(add_clicks, remove_clicks, cumul_ingreds_json,
                                 ingredient, amt, units, nutrients_json):
    """
    add row to cumulative ingredients for n_clicks of add ingredient
    data is a list of dicts of [{col: value, col: value}, {col: value, col: value}]
    https://community.plotly.com/t/callback-for-deleting-a-row-in-a-data-table/21437/4?u=nyck33
    remove: get data from DataTable, make df and update hidden div
    """
    ctx = callback_context
    # get id of trigger
    trigger = ctx.triggered[0]['prop_id'].split(".")[0]
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if add_clicks <= 0:
        return no_update
    # make a dict of current ingred, amt, units and append
    if trigger == "add-ingredient":
        curr_ingred_dict = {'Ingredient': ingredient, 'Amount': str(amt), 'Units': units}
        curr_ingred_df = pd.DataFrame(curr_ingred_dict, columns=['Ingredient', 'Amount', 'Units'],
                                      index=[0])
        if cumul_ingreds_json is not None:
            cumul_ingreds_df = pd.read_json(cumul_ingreds_json, orient='split')
            # reorder
            cumul_ingreds_df = cumul_ingreds_df[['Ingredient', 'Amount', 'Units']]
            new_cumul_ingreds_df = pd.concat([cumul_ingreds_df, curr_ingred_df])
            # cumul_ingreds_dicts_arr = cumul_ingreds_df.to_dict('records')
            # cumul_ingreds_dicts_arr.append(curr_ingred_dict)
            # new_cumul_ingreds_df = pd.DataFrame(cumul_ingreds_dicts_arr)
            new_cumul_ingreds_cols = [{"name": i, "id": i} for i in new_cumul_ingreds_df.columns]
            new_cumul_ingreds_data = new_cumul_ingreds_df.to_dict('records')

        else:  # first added ingredient
            new_cumul_ingreds_df = pd.DataFrame([curr_ingred_dict],
                                                columns=['Ingredient', 'Amount', 'Units'])
            # new_cumul_ingreds_df = pd.DataFrame([curr_ingred_dict], columns=curr_ingred_dict.keys())
            new_cumul_ingreds_cols = [{"name": i, "id": i} for i in new_cumul_ingreds_df.columns]
            # todo: hardcode dict into list for one record???
            new_cumul_ingreds_data = new_cumul_ingreds_df.to_dict('records')

        # todo: return this to hidden div
        new_cumul_ingreds_json = new_cumul_ingreds_df.to_json(date_format='iso', orient='split')

        return new_cumul_ingreds_json, new_cumul_ingreds_data, new_cumul_ingreds_cols

    elif trigger == "remove-ingredient":
        # make df from table data, upload to hidden div and return as data and cols
        # account for two types of delete, selection and button press and native UI delete
        pass
    return no_update, no_update, no_update



"""
@app.callback(
    Output('rdi-figure', 'figure'),
    Input('radio', 'value')

)
def compare_with_rdi(radio_btn_clicked):
    '''
    show graphs for cnf vs rdi: elements, vitamins, macronutrients
    for one ingredient in search box
    input is radio button and show graphs vs rdi button
    if one ingredient:
        show graphs for one vs rdi
    elif all ingredients:
        show graphs for all ingreds vs rdi
    '''

    # make dict of rdi nutrient name: unit

    #dict of cnf nutrient names
    nutrients = CNFNutrientName.objects
    cnf_nutr_dict = {}
    for n in nutrients:
        cnf_nutr_dict[str(n.name)] = str(n.unit)
    # check nutrient names

return app.server
"""








