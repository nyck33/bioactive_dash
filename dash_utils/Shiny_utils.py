"""
match rdi with cnf
"""
import numpy as np
import os, re
from pathlib import Path
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from mongoengine import connect
#connect('cnf')
from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
        CNFYieldAmount, CNFRefuseAmount, CNFNutrientName
)
from models.model_nutrients import (
            ElementsRDI, VitaminsRDI, ElementsUpperRDI,
            VitaminsUpperRDI, MacronutrientsDistRange
        )
from models.model_infantsRDI import (
    InfantsElementsRDI, InfantsVitaminsRDI, InfantsMacroRDI, InfantsElementsUpperRDI,\
        InfantsVitaminsUpperRDI
)
from models.model_childrenRDI import (
    ChildrenElementsRDI, ChildrenVitaminsRDI, ChildrenMacroRDI, ChildrenElementsUpperRDI,\
        ChildrenVitaminsUpperRDI
)
from models.model_malesRDI import (
    MalesElementsRDI, MalesVitaminsRDI, MalesMacroRDI, MalesElementsUpperRDI, MalesVitaminsUpperRDI
)
from models.model_femalesRDI import (
    FemalesElementsRDI, FemalesVitaminsRDI, FemalesMacroRDI, FemalesElementsUpperRDI,\
        FemalesVitaminsUpperRDI
)
from models.model_pregnancyRDI import (
    PregnancyElementsRDI, PregnancyVitaminsRDI, PregnancyMacroRDI, PregnancyElementsUpperRDI,\
        PregnancyVitaminsUpperRDI
)
from models.model_lactationRDI import (
    LactationElementsRDI, LactationVitaminsRDI, LactationMacroRDI, LactationElementsUpperRDI,\
        LactationVitaminsUpperRDI
)

# todo: use this for cumulation
rdi_nutrients = {
    'water': "", "fat": "", 'fiber': "", 'linoleicAcid': "", 'alphaLinolenicAcid': "",
    'carbohydrate': "", 'protein': "",
    'calcium': "", 'chromium': "", 'copper': "", 'fluoride': "", 'iodine': "", 'iron': "",
    'magnesium': "",
    'manganese': "", 'molybdenum': "", 'phosphorus': "", 'selenium': "", 'zinc': "",
    'potassium': "",
    'sodium': "", 'chloride': "",
    'vitaminA': "", 'vitaminC': "", 'vitaminD': "", 'vitaminE': "", 'vitaminK': "", 'thiamin': "",
    'riboflavin': "", 'niacin': "", 'vitaminB6': "", 'folate': "", 'vitaminB12': "",
    'pantothenicAcid': "", 'biotin': "", 'choline': ""
}

rdi_modelnames_arr = [
    'MacronutrientsDistRange',
    'InfantsElementsRDI', 'InfantsVitaminsRDI', 'InfantsMacroRDI', 'InfantsElementsUpperRDI',
    'InfantsVitaminsUpperRDI',
    'ChildrenElementsRDI', 'ChildrenVitaminsRDI', 'ChildrenMacroRDI',
    'ChildrenElementsUpperRDI',
    'ChildrenVitaminsUpperRDI',
    'MalesElementsRDI', 'MalesVitaminsRDI', 'MalesMacroRDI', 'MalesElementsUpperRDI',
    'MalesVitaminsUpperRDI',
    'FemalesElementsRDI', 'FemalesVitaminsRDI', 'FemalesMacroRDI', 'FemalesElementsUpperRDI',
    'FemalesVitaminsUpperRDI',
    'PregnancyElementsRDI', 'PregnancyVitaminsRDI', 'PregnancyMacroRDI',
    'PregnancyElementsUpperRDI',
    'PregnancyVitaminsUpperRDI',
    'LactationElementsRDI', 'LactationVitaminsRDI', 'LactationMacroRDI',
    'LactationElementsUpperRDI',
    'LactationVitaminsUpperRDI'
]

def make_food_to_id_dict():
    """
    call this right away
    """
    food_name_query_set = CNFFoodName.objects(description__exists=True)
    food_names_arr = []
    food_ids_arr = []


    for food in food_name_query_set:
        '''
        # dict with description as key, values: id, group, source
        food_dict[food['description']] = [food['id'], food['food_group'],
                                          food['food_source'],
                                          food['scientific_name']]
        '''
        food_names_arr.append(food['description'])
        food_ids_arr.append(food['id'])

    #assert len(food_names_arr) == len(food_ids)

    food_to_id_dict = dict(zip(food_names_arr, food_ids_arr))

    return food_to_id_dict, food_names_arr, food_ids_arr

#global helper fn
def get_unit_names(food_id):
    """
    class_collection: one of the CNF collections
    get the unit names and return after cleaning and keeping only unique
    """
    # get units
    conversions = CNFConversionFactor.objects.filter(food=str(food_id))
    unit_names = []
    for c in conversions:
        unit_names.append(c.measure.name)
    #print(f'unit_names {unit_names}')
    # take out the numbers and whitespace
    # todo: pattern has to include all non-alpha
    pattern = '[0-9]'
    temp_arr = [re.sub(pattern, '', x) for x in unit_names]
    unit_names = [x.strip() for x in temp_arr]
    # only keep the unique measure names
    measure_set = set(unit_names)
    unit_names = list(measure_set)

    return unit_names

def make_foodgroup_df(food_id):
    """
    ("Group"), html.Th("Source"), html.Th("Scientific Name")])
    """

    food = CNFFoodName.objects.get(id=str(food_id))
    food_grp = food.food_group.name
    food_src = food.food_source.description
    food_sci_name = "n/a"
    if food.scientific_name:
        food_sci_name = food.scientific_name
    foodgroup_df = pd.DataFrame(
        {'Group': [food_grp],
         "Source": [food_src],
         "Scientific Name": [food_sci_name]
         }
    )
    return foodgroup_df


def make_conversions_df(food_id):
    """
    param
    """
    food = CNFFoodName.objects.get(id=str(food_id))
    conversions = CNFConversionFactor.objects.filter(food=food)
    measure_names = []
    measure_vals = []
    for c in conversions:
        measure_names.append(c.measure.name)
        measure_vals.append(c.value)

    conversions_df = pd.DataFrame(
        {'Name': measure_names,
         'Multiplier': measure_vals
         })

    return conversions_df

#global helper fn
def make_nutrients_df(food_id):
    food = CNFFoodName.objects.get(id=str(food_id))
    nutrients = CNFNutrientAmount.objects.filter(food=food, nutrient_value__gt=0)

    nutrient_names = []
    nutrient_vals = []
    nutrient_units = []

    for n in nutrients:
        nutrient_names.append(n.nutrient_name.name)
        nutrient_vals.append(n.nutrient_value)
        nutrient_units.append(n.nutrient_name.unit)

    nutrients_df = pd.DataFrame(
        {"Name": nutrient_names,
         "Value": nutrient_vals,
         "Units": nutrient_units
         })

    return nutrients_df

def get_conversions_multiplier(conversions_df, units):
    curr_multiplier = ''
    measure_num = -1
    measure_name = ''
    for index, row in conversions_df.iterrows():
        if units in str(row['Name']):
            # get number
            measure_name = str(row['Name'])
            measure_num = float(re.findall("\d+", measure_name)[0])
            curr_multiplier = float(row['Multiplier'])
            break
    return curr_multiplier, measure_num

def mult_nutrients_df(nutrients_df,curr_multiplier, measure_num, amt):
    new_nutrients_df = nutrients_df.copy()
    new_nutrients_df.set_index('Name', inplace=True, drop=False)
    multiplier_factor = (float(amt)) / measure_num
    new_multiplier = multiplier_factor * curr_multiplier

    # multiply all nutrients by new_multiplier
    for index, row in nutrients_df.iterrows():
        row_val = float(row['Value']) * new_multiplier
        #nutrients_df.row['Value'] = str(new_row_val)
        row_name = row['Name']
        new_nutrients_df.loc[[row_name], ['Value']] = str(row_val)

    return new_nutrients_df






