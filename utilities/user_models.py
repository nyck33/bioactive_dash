from flask_mongoengine import MongoEngine
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, BooleanField, validators
from flask import current_app as app
import datetime
#with cnf.app_context():
#db = app.db
from app.extensions import db

# Define User document
# NB: Make sure to add flask_user UserMixin
class User(db.Document, UserMixin):
    #email_confirmed_at = cnf.db.StringField('confirmed at', datetime.datetime.now())
    active = db.BooleanField(default=True)
    date_joined = db.DateTimeField(default=datetime.datetime.utcnow)
    # User info
    first_name = db.StringField(max_length=50, default='')
    last_name = db.StringField(max_length=50, default='')
    email = db.StringField(max_length=50, default='')
    # User authentication info
    username = db.StringField(max_length=50, required=True, default='')
    password = db.StringField(required=True, default='')
    # Relationships
    roles = db.ListField(db.StringField(), default=[])
    #weekly minerals
    # mg/d = m, ug/d = u, g/d = g
    calcium_wk = db.StringField(default='')  # m
    chromium_wk = db.StringField(default='')  # u
    copper_wk = db.StringField(default="")  # u
    fluoride_wk = db.StringField(default='')  # m
    iodine_wk = db.StringField(default='')  # u
    iron_wk = db.StringField(default='')  # m
    magnesium_wk = db.StringField(default='')  # m
    manganese_wk = db.StringField(default='')  # u
    molybdenum_wk = db.StringField(default="")  # u
    phosphorus_wk = db.StringField(default='')  # m
    selenium_wk = db.StringField(default='')  # u
    zinc_wk = db.StringField(default='')  # m
    potassium_wk = db.StringField(default='')  # m
    sodium_wk = db.StringField(default='')  # m
    chloride_wk = db.StringField(default='')  # g
    # wkly vitamins
    # wkly vitamins
    # mg/d = m, ug/d = u, g/d = g
    vitaminA_wk = db.StringField(default='')  # u
    vitaminC_wk = db.StringField(default='')  # m
    vitaminD_wk = db.StringField(default="")  # u
    vitaminE_wk = db.StringField(default='')  # m
    vitaminK_wk = db.StringField(default='')  # u
    thiamin_wk = db.StringField(default='')  # m
    riboflavin_wk = db.StringField(default='')  # m
    niacin_wk = db.StringField(default='')  # m
    vitaminB6_wk = db.StringField(default="")  # m
    folate_wk = db.StringField(default='')  # u
    vitaminB12_wk = db.StringField(default='')  # u
    pantothenicAcid_wk = db.StringField(default='')  # m
    biotin_wk = db.StringField(default='')  # m
    choline_wk = db.StringField(default='')  # m
    #macroNutrients week
    total_water_wk = db.DecimalField(default=0.0)
    carbs_wk = db.IntField(default=0)
    total_fiber_wk = db.IntField(default=0)
    fat_wk = db.IntField(default=0)
    linoleicAcid_wk = db.DecimalField(default=0.0)
    alphaLinolenicAcid_wk = db.DecimalField(default=0.0)
    protein_wk = db.DecimalField(default=0.0)

#Roles and UsersRoles add later


#Define User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')
    ])
    submit = SubmitField('Save')

