"""
infant, child, male, female, preg, lactation for all plus macroUpper
so 6 groups, 2 classes for each (RDI, upper limits) plus this table of
Acceptable MacroNutrient Distribution Ranges for children 1-3, 4-18 and adults

"""
from flask import current_app as app


# Just a shorthand
#db = app.db  # MongoEngine(cnf) in main.py
from app import db


class NutrientsDocument(db.Document):
    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }


class MacroDistRange(NutrientsDocument):
    meta={
        'collection': 'MacroDistRange'
    }
    life_stage_grp = db.StringField()
    fat = db.StringField()
    linoleicAcid = db.StringField()
    alphaLinolenicAcdi =db.StringField()
    carbs = db.StringField()
    protein = db.StringField()

'''
class ChildrenU4MacroDistRange(NutrientsDocument):
    meta = {
        'collection': 'ChidrenU14MacroDistRange'
    }
    fat = db.StringField()
    linoleicAcid = db.StringField()
    alphaLinolenicAcid = db.StringField()
    carbs = db.StringField()
    protein = db.StringField()


class ChildrenU18MacroDistRange(NutrientsDocument):
    meta={
        'collection': 'ChildrenU18MacroDistRange'
    }
    fat = db.StringField()
    linoleicAcid = db.StringField()
    alphaLinolenicAcid = db.StringField()
    carbs = db.StringField()
    protein = db.StringField()


class AdultsMacroDistRange(NutrientsDocument):
    meta={
        'collection': 'AdultsMacroDistRange'
    }
    fat = db.StringField()
    linoleicAcid = db.StringField()
    alphaLinolenicAcid = db.StringField()
    carbs = db.StringField()
    protein = db.StringField()

'''