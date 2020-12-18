"""
infant, child, male, female, preg, lactation for all plus macroUpper
so 6 * 5 classes + 3 for macroDistRange of 1-3, 4-18 and adults
total 33 classes = 33 collections
"""
from flask import current_app as app
from cnf.models.model_macronutrients_distrange import NutrientsDocument
# Just a shorthand
db = app.db  # MongoEngine(cnf) in main.py


class ElementsRDI(NutrientsDocument):
    meta = {
        'collection': 'infant_mineralsRDI'
    }
    #mg/d = m, ug/d = u, g/d = g
    calcium = db.StringField(default='') #m
    chromium = db.StringField(default='') #u
    copper = db.StringField(default="") #u
    fluoride = db.StringField(default='') #m
    iodine = db.StringField(default='') #u
    iron = db.StringField(default= '') #m
    magnesium = db.StringField(default='')  # m
    manganese = db.StringField(default='')  # u
    molybdenum = db.StringField(default="")  # u
    phosphorus = db.StringField(default='')  # m
    selenium = db.StringField(default='')  # u
    zinc = db.StringField(default='') #m
    potassium = db.StringField(default='')  # m
    sodium = db.StringField(default='')  # m
    chloride = db.StringField(default='')  # g