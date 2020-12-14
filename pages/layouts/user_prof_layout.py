import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
from flask_login import current_user
#from app import user_id
from sqlalchemy import select, Table, MetaData
from utilities.config import engine


person_type_arr = ['infant', 'child', 'male', 'female', 'pregnant', 'lactating']
life_stage_arr= ['< 6 mo', '< 12 mo', '1 to 3 y', '4 to 8 y', '9 to 13 y',
                       '14 to 18 y', '19 to 30 y', '31 to 50 y', '51 to 70 y',
                       '> 70 y']

'''
def get_current_lifestage():

    user_id = ''
    email = ''
    if current_user and current_user.is_authenticated:
        user_id = current_user.id
        email = current_user.email

    conn = engine.connect()
    metadata = MetaData()
    user = Table('user', metadata, autoload=True, autoload_with=engine)
    stmt = select([user])
    stmt = stmt.where(user.columns.id == user_id)
    result = conn.execute(stmt).fetchall()
    age, person_type, lifestage = '', '', ''
    for res in result:
        age = res.age
        person_type = res.person_type
        lifestage = res.lifestage_grp

    current_lifestage_str = f'Current Stats: Age: {age}, Type: {person_type}, Lifestage: {lifestage} '

    return current_lifestage_str
'''

user_prof_layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                # user lifestage group
                # age
                dbc.Button(
                    id='current-lifestage-btn',
                    style={'display': 'none'},
                    n_clicks=1
                ),
                html.Div(
                    #get_current_lifestage(),
                    id='current-lifestage'
                ),
                html.Br(),
                dbc.Label('Age:', id='profile-age'),
                dbc.Input(placeholder='Enter age...',
                          id='profile-age-input',
                          type='number'),
                html.Br(),

                # person_type
                dbc.Label('Person Type:', id='profile-person-type'),
                dcc.Dropdown(
                    id='person-type-dropdown',
                    options=[{'label': person, 'value': person} for person in person_type_arr],
                    value=person_type_arr[0]
                ),
                html.Br(),

                html.Div(
                    id='life-stage-dropdown-loc'
                ),
            ])
        ], width=6)
    ])
], id="user-prof-layout", style={'display': 'block'})

