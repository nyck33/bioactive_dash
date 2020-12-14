import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
from flask_login import current_user
import time
import pandas as pd
import json
from utilities.config import engine
from sqlalchemy import MetaData, select, Table, insert
#make queries to get current lifestage data

from server import app
from pages.layouts.user_prof_layout import (user_prof_layout,
person_type_arr, life_stage_arr)

def register_home_callbacks(app):
    @app.callback(
        Output('home-test', 'children'),
        [Input('home-test-trigger', 'children')]
    )
    def home_test_update(trigger):
        '''
        updates arbitrary value on home page for test
        '''
        time.sleep(2)
        return html.Div('after the update', style=dict(color='red'))

    @app.callback(
        Output('life-stage-dropdown-loc', 'children'),
        [Input('person-type-dropdown', 'value')]
    )
    def build_lifestage_ui(person_type):

        conn = engine.connect()
        metadata = MetaData()
        if person_type == 'infant':
            return html.Div([
                dbc.Label('Life-Stage Group:', id='profile-lifestage'),
                dcc.Dropdown(
                    id='lifestage-dropdown',
                    options=[{'label': lifestage, 'value': lifestage} for lifestage in life_stage_arr[:2]],
                    value=life_stage_arr[0]
                ),
                html.Br(),
                dbc.Button(
                    "Submit",
                    id='lifestage-btn',
                    color='primary'
                )
            ])
        elif person_type == 'child':
            return html.Div([
                dbc.Label('Life-Stage Group:', id='profile-lifestage'),
                dcc.Dropdown(
                    id='lifestage-dropdown',
                    options=[{'label': lifestage, 'value': lifestage} for lifestage in life_stage_arr[2:4]],
                    value=life_stage_arr[0]
                ),
                html.Br(),
                dbc.Button(
                    "Submit",
                    id='lifestage-btn',
                    color='primary'
                )
            ])
        elif person_type == 'male' or person_type == 'female':
            return html.Div([
                dbc.Label('Life-Stage Group:', id='profile-lifestage'),
                dcc.Dropdown(
                    id='lifestage-dropdown',
                    options=[{'label': lifestage, 'value': lifestage} for lifestage in life_stage_arr[4:]],
                    value=life_stage_arr[0]
                ),
                html.Br(),
                dbc.Button(
                    "Submit",
                    id='lifestage-btn',
                    color='primary'
                )
            ])
        elif person_type == 'pregnant' or person_type == 'lactating':
            return html.Div([
                dbc.Label('Life-Stage Group:', id='profile-lifestage'),
                dcc.Dropdown(
                    id='lifestage-dropdown',
                    options=[{'label': lifestage, 'value': lifestage} for lifestage in life_stage_arr[5:8]],
                    value=life_stage_arr[0]
                ),
                html.Br(),
                dbc.Button(
                    "Submit",
                    id='lifestage-btn',
                    color='primary'
                )
            ])
        return html.Div("Error")

    @app.callback(
        Output('save-confirm-out', 'children'),
        Input('lifestage-btn', 'n_clicks'),
        [State('profile-age-input', 'value'),
        State('person-type-dropdown', 'value'),
         State('lifestage-dropdown', 'value')]
    )
    def save_lifestage(save_clicks, age, person, lifestage):
        user_id = -1
        if save_clicks is None or save_clicks <=0:
            return no_update
        if current_user.is_authenticated:
            user_id = current_user.id
        #todo use update
        conn = engine.connect()
        metadata=MetaData()
        user = Table('user', metadata, autoload=True, autoload_with=engine)
        stmt = user.update().where(user.columns.id==user_id).\
            values(age=age, person_type=person, lifestage_grp=lifestage)
        conn.execute(stmt)
        save_confirm_msg = ''
        save_confirm_msg = f'updated {age}, {person}, {lifestage}'

        return save_confirm_msg

    @app.callback(
        Output('current-lifestage', 'children'),
        Input('current-user-store', 'data')
    )
    def get_current_lifestage(user_json):
        if user_json is None:
            return no_update

        user_dict = json.loads(user_json)
        user_id = user_dict['id']
        conn = engine.connect()
        metadata = MetaData()
        user = Table('user', metadata, autoload=True, autoload_with=engine)
        stmt = select([user])
        stmt = stmt.where(user.columns.id==user_id)
        result = conn.execute(stmt).fetchall()
        age, person_type, lifestage = '', '', ''
        for res in result:
            age = res.age
            person_type = res.person_type
            lifestage = res.lifestage_grp

        current_lifestage_str = f'Current Stats: Age: {age}, Type: {person_type}, Lifestage: {lifestage} '

        return current_lifestage_str


