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

def register_make_meal_callbacks(app):
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

        #todo: take out this button, add-ingred to see nutrient totals
        elif trigger == 'update-nut-table-btn' and add_clicks > 0:
            # must use base table for math
            # nutrients_df = make_nutrients_df(food_id)
            nutrients_df = pd.read_json(nutrients_json, orient='split')
            conversions_df = pd.read_json(conversions_json, orient='split')
            curr_multiplier, measure_num = get_conversions_multiplier(conversions_df, units)
            # divide amount/measure_num
            nutrients_df = mult_nutrients_df(nutrients_df, curr_multiplier, measure_num, amt)
            #todo: update the datatable but leave out nutrients_json
            nutrients_cols = [{"name": i, "id": i} for i in nutrients_df.columns]
            nutrients_data = nutrients_df.to_dict('records')

            nutrients_json = nutrients_df.to_json(date_format='iso', orient='split')

            return no_update, nutrients_json, no_update, no_update, no_update, \
                   no_update, nutrients_data, nutrients_cols, 'update nutrients table', ctx_msg

            #return no_update, nutrients_json, no_update, no_update, no_update, no_update, nutrients_data, nutrients_cols, \
             #      'update nutrients table', ctx_msg

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
               'none updated', ctx_msg

    #todo: this is chained by the callback below it

    ################def update_total_nutrients_df was here################3
    @app.callback(
        [Output('cumul-ingreds-table', 'data'),
         Output('cumul-ingreds-table', 'columns')],
        [Input('hidden-cumul-ingreds-df', 'children')]
    )
    def update_cumul_ingreds_table(cumul_ingreds_json):
        if cumul_ingreds_json is None:
            return no_update, no_update
        cumul_ingreds_data = {}
        cumul_ingreds_cols = [{}]
        if cumul_ingreds_json is not None:
            cumul_ingreds_df = pd.read_json(cumul_ingreds_json, orient='split')
            # reorder
            cumul_ingreds_df = cumul_ingreds_df[['Ingredient', 'Amount', 'Units']]
            cumul_ingreds_cols = [{"name": i, "id": i} for i in cumul_ingreds_df.columns]
            cumul_ingreds_data = cumul_ingreds_df.to_dict('records')

        return cumul_ingreds_data, cumul_ingreds_cols

    # for display at the top
    @app.callback(
        [Output('hidden-cumul-ingreds-df', 'children'),
         #Output('cumul-ingreds-table', 'data'),
         #Output('cumul-ingreds-table', 'columns'),
        Output('hidden-total-nutrients-df', 'data'), #new
         Output('cnf-totals-table', 'data'), #new
         Output('cnf-totals-table', 'columns')], #new
        [Input('add-ingredient', 'n_clicks'), #same
         Input('cumul-ingreds-table','data')], #todo: dummy
        [State('hidden-cumul-ingreds-df', 'children'),
         State('search-ingredient', 'value'),
         State("numerical-amount", "value"),
         State('units-dropdown', 'value'),
         State('hidden-nutrients-df', 'data'), #same
         State('hidden-total-nutrients-df', 'data')] #same
    )
    #todo: update the dataframe and chain to update table
    def update_ingreds_df_nut_totals_tbl(add_clicks, del_row_data, cumul_ingreds_json,
                                     ingredient, amt, units, nutrients_json,
                                     total_nutrients_json):
        """
        add row to cumulative ingredients for n_clicks of add ingredient
        data is a list of dicts of [{col: value, col: value}, {col: value, col: value}]
        https://community.plotly.com/t/callback-for-deleting-a-row-in-a-data-table/21437/4?u=nyck33
        remove: get data from DataTable, make df and update hidden div
        """
        ctx = callback_context
        # get id of trigger
        trigger = ctx.triggered[0]['prop_id'].split(".")[0]
        print(f"cum-ingreds-tbl trigger: {trigger}")
        ctx_msg = json.dumps({
            'states': ctx.states,
            'triggered': ctx.triggered,
            'inputs': ctx.inputs
        }, indent=2)
        if add_clicks <= 0:
            return no_update, no_update, no_update, no_update, no_update, no_update
        # make a dict of current ingred, amt, units and append
        if trigger == "add-ingredient":
            #todo: update the total nutrients_df first with new entry, then add to cumulative list
            nutrients_totals_df = None
            if total_nutrients_json is None:
                nutrients_totals_df = pd.concat({k: pd.Series(v) for k, v in
                                                 nutrients_totals_dict.items()}, axis=1)
            else:
                # add to this
                nutrients_totals_df = pd.read_json(total_nutrients_json, orient='split')

            if nutrients_json is None: # todo: no entry in fields?
                return no_update, no_update, no_update, no_update

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
            ###################################################################################
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
                #new_cumul_ingreds_cols = [{"name": i, "id": i} for i in new_cumul_ingreds_df.columns]
                #new_cumul_ingreds_data = new_cumul_ingreds_df.to_dict('records')

            else:  # first added ingredient
                new_cumul_ingreds_df = pd.DataFrame([curr_ingred_dict],
                                                    columns=['Ingredient', 'Amount', 'Units'])
                # new_cumul_ingreds_df = pd.DataFrame([curr_ingred_dict], columns=curr_ingred_dict.keys())
                #new_cumul_ingreds_cols = [{"name": i, "id": i} for i in new_cumul_ingreds_df.columns]

                #new_cumul_ingreds_data = new_cumul_ingreds_df.to_dict('records')

            # return this to hidden div
            new_cumul_ingreds_json = new_cumul_ingreds_df.to_json(date_format='iso', orient='split')

            return new_cumul_ingreds_json, \
                    total_nutrients_json, cnf_totals_table_data, cnf_totals_table_cols

        elif trigger == "cumul-ingreds-table": #row removed
            new_cumul_ingreds_json = {}
            cnf_totals_table_data = {}
            cnf_totals_table_cols = [{}]
            #subtract from this
            nutrients_totals_df = pd.read_json(total_nutrients_json, orient='split')
            # make df from table data, upload to hidden div
            new_cumul_ingreds_df = pd.DataFrame(del_row_data)
            new_cumul_ingreds_json = new_cumul_ingreds_df.to_json(date_format='iso', orient='split')

            # must update cnf_totals table data, cols, total nutrients json
            # get the cumul_ingreds_json compare to new_cumul_ingreds_df
            # find item that was deleted, do the math to subtract nut amounts
            # from total_nutrients_json and make cnf_totals_data and cols
            before_cum_ingreds_df = pd.read_json(cumul_ingreds_json, orient='split')
            before_ingreds_arr = before_cum_ingreds_df['Ingredient'].tolist()
            now_ingreds_arr = new_cumul_ingreds_df['Ingredient'].tolist()
            # compare these two, might be more than one
            removed = list(set(before_ingreds_arr) - set(now_ingreds_arr))
            #get quantities of nutrients for each deleted ingredient
            for ingred in removed:
                ingred_row = before_cum_ingreds_df.loc[before_cum_ingreds_df['Ingredient']==ingred]
                # extract value from col series
                amt = ingred_row['Amount'].item()
                units = ingred_row['Units'].item()
                # call fn to get df of removed nut vals for curr_ingred
                food_id = food_to_id_dict[ingred]
                nutrients_df = make_nutrients_df(food_id)
                conversions_df = make_conversions_df(food_id)
                curr_multiplier, measure_num = get_conversions_multiplier(conversions_df, units)
                rem_nutrients_df = mult_nutrients_df(nutrients_df, curr_multiplier, measure_num, amt)

                # for each nutrient in df, cols = "Name", "Value", "unit"
                # find Name in current nut_totals_table and subtract Value from Amount
                for index, row in rem_nutrients_df.iterrows():
                    nut = row['Name']
                    amt = float(row['Value'])
                    units = row['Units']
                    curr_row = nutrients_totals_df.loc[nutrients_totals_df['Name']==nut]
                    #curr_amt = float(nutrients_totals_df.loc[nutrients_totals_df['Name']==curr_nut, 'Value'])
                    curr_amt = curr_row['Value'].item()
                    new_amt = str(curr_amt - amt)

                    nutrients_totals_df.loc[[nut], ['Value']] = new_amt

            cnf_totals_table_data = nutrients_totals_df.to_dict('records')
            cnf_totals_table_cols = [{'name': i, "id": i} for i in nutrients_totals_df.columns]

        return new_cumul_ingreds_json, \
               total_nutrients_json, cnf_totals_table_data, cnf_totals_table_cols

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








