"""
infant, child, male, female, preg, lactation for all plus macroUpper
so 6 groups, 2 classes for each (RDI, upper limits) plus this table of
Acceptable MacroNutrient Distribution Ranges for children 1-3, 4-18 and adults

"""
from flask import current_app as app
from .model_nutrients import NutrientsDocument
# Just a shorthand
#db_mongo = app.db_mongo  # MongoEngine(cnf) in main.py
from .db_setup import db_mongo


class FemalesElementsRDI(NutrientsDocument):
    """
    elements, vitamins, macro
    """
    meta = {
        'collection': 'FemalesElementsRDI'
    }
    # mg/d = m, ug/d = u, g/d = g
    life_stage_grp = db_mongo.StringField(default="")
    calcium = db_mongo.StringField(default='')  # m
    chromium = db_mongo.StringField(default='')  # u
    copper = db_mongo.StringField(default="")  # u
    fluoride = db_mongo.StringField(default='')  # m
    iodine = db_mongo.StringField(default='')  # u
    iron = db_mongo.StringField(default='')  # m
    magnesium = db_mongo.StringField(default='')  # m
    manganese = db_mongo.StringField(default='')  # u
    molybdenum = db_mongo.StringField(default="")  # u
    phosphorus = db_mongo.StringField(default='')  # m
    selenium = db_mongo.StringField(default='')  # u
    zinc = db_mongo.StringField(default='')  # m
    potassium = db_mongo.StringField(default='')  # m
    sodium = db_mongo.StringField(default='')  # m
    chloride = db_mongo.StringField(default='')  # g


class FemalesVitaminsRDI(NutrientsDocument):
    """
    elements, vitamins, macro
    """
    meta = {
        'collection': 'FemalesVitaminsRDI'
    }
    # mg/d = m, ug/d = u, g/d = g
    life_stage_grp = db_mongo.StringField(default="")

    vitaminA = db_mongo.StringField(default='')  # u
    vitaminC = db_mongo.StringField(default='')  # m
    vitaminD = db_mongo.StringField(default="")  # u
    vitaminE = db_mongo.StringField(default='')  # m
    vitaminK = db_mongo.StringField(default='')  # u
    thiamin = db_mongo.StringField(default='')  # m
    riboflavin = db_mongo.StringField(default='')  # m
    niacin = db_mongo.StringField(default='')  # m
    vitaminB6 = db_mongo.StringField(default="")  # m
    folate = db_mongo.StringField(default='')  # u
    vitaminB12 = db_mongo.StringField(default='')  # u
    pantothenicAcid = db_mongo.StringField(default='')  # m
    biotin = db_mongo.StringField(default='')  # m
    choline = db_mongo.StringField(default='')  # m


class FemalesMacroRDI(NutrientsDocument):
    meta={
        'collection': 'FemalesMacroRDI'
    }
    life_stage_grp = db_mongo.StringField(default="")

    total_water = db_mongo.StringField()
    carbs = db_mongo.StringField()
    total_fiber = db_mongo.StringField()
    fat = db_mongo.StringField()
    linoleicAcid = db_mongo.StringField()
    alphaLinolenicAcid = db_mongo.StringField()
    protein = db_mongo.StringField()


class FemalesElementsUpperRDI(NutrientsDocument):
    """
    elements, vitamins, macro
    """
    meta = {
        'collection': 'FemalesElementsUpperRDI'
    }
    # mg/d = m, ug/d = u, g/d = g
    life_stage_grp = db_mongo.StringField(default="")
    calcium = db_mongo.StringField(default='')  # m
    chromium = db_mongo.StringField(default='')  # u
    copper = db_mongo.StringField(default="")  # u
    fluoride = db_mongo.StringField(default='')  # m
    iodine = db_mongo.StringField(default='')  # u
    iron = db_mongo.StringField(default='')  # m
    magnesium = db_mongo.StringField(default='')  # m
    manganese = db_mongo.StringField(default='')  # u
    molybdenum = db_mongo.StringField(default="")  # u
    phosphorus = db_mongo.StringField(default='')  # m
    selenium = db_mongo.StringField(default='')  # u
    zinc = db_mongo.StringField(default='')  # m
    potassium = db_mongo.StringField(default='')  # m
    sodium = db_mongo.StringField(default='')  # m
    chloride = db_mongo.StringField(default='')  # g

class FemalesVitaminsUpperRDI(NutrientsDocument):
    """
    elements, vitamins, macro
    """
    meta = {
        'collection': 'FemalesVitaminsUpperRDI'
    }
    # mg/d = m, ug/d = u, g/d = g
    life_stage_grp = db_mongo.StringField(default="")

    vitaminA = db_mongo.StringField(default='')  # u
    vitaminC = db_mongo.StringField(default='')  # m
    vitaminD = db_mongo.StringField(default="")  # u
    vitaminE = db_mongo.StringField(default='')  # m
    vitaminK = db_mongo.StringField(default='')  # u
    thiamin = db_mongo.StringField(default='')  # m
    riboflavin = db_mongo.StringField(default='')  # m
    niacin = db_mongo.StringField(default='')  # m
    vitaminB6 = db_mongo.StringField(default="")  # m
    folate = db_mongo.StringField(default='')  # u
    vitaminB12 = db_mongo.StringField(default='')  # u
    pantothenicAcid = db_mongo.StringField(default='')  # m
    biotin = db_mongo.StringField(default='')  # m
    choline = db_mongo.StringField(default='')  # m



