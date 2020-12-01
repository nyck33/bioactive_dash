"""
infant, child, male, female, preg, lactation for all plus macroUpper
so 6 * 5 classes + 3 for macroDistRange of 1-3, 4-18 and adults
total 33 classes = 33 collections
"""
from flask import current_app as app
from cnf.models.model_macronutrients_distrange import NutrientsDocument
# Just a shorthand
db = app.db  # MongoEngine(cnf) in main.py

class UpperElementsRDI(NutrientsDocument):
    meta = {
        'collection': 'upperMineralsRDI'
    }
    # mg/d = m, ug/d = u, g/d = g
    arsenic = db.StringField(default='')
    boron = db.StringField(default='')
    calcium = db.StringField(default='')  # m
    chromium = db.StringField(default='')  # u
    copper = db.StringField(default="")  # u
    fluoride = db.StringField(default='')  # m
    iodine = db.StringField(default='')  # u
    iron = db.StringField(default='')  # m
    magnesium = db.StringField(default='')  # m
    manganese = db.StringField(default='')  # u
    molybdenum = db.StringField(default="")  # u
    nickel = db.StringField(default='') #mg
    phosphorus = db.StringField(default='')  # m
    potassium = db.StringField(default="")
    selenium = db.StringField(default='')  # u
    silicon = db.StringField(default='')
    sulfate = db.StringField(default='')
    vanadium = db.StringField(default='')
    zinc = db.StringField(default='')  # m
    sodium = db.StringField(default='')  # m
    chloride = db.StringField(default='')  # g


class UpperVitaminsRDI(NutrientsDocument):
    meta = {
        'collection': 'upperVitaminsRDI'
    }
    # mg/d = m, ug/d = u, g/d = g
    vitaminA = db.StringField(default='')  # u
    vitaminC = db.StringField(default='')  # m
    vitaminD = db.StringField(default="")  # u
    vitaminE = db.StringField(default='')  # m
    vitaminK = db.StringField(default='')  # u
    thiamin = db.StringField(default='')  # m
    riboflavin = db.StringField(default='')  # m
    niacin = db.StringField(default='')  # m
    vitaminB6 = db.StringField(default="")  # m
    folate = db.StringField(default='')  # u
    vitaminB12 = db.StringField(default='')  # u
    pantothenicAcid = db.StringField(default='')  # m
    biotin = db.StringField(default='')  # m
    choline = db.StringField(default='')  # m
    carotenoids = db.StringField(default='') #all ND