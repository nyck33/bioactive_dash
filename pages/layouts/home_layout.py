import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

#todo: use dicts here
person_type_arr = ['infant', 'child', 'male', 'female', 'pregnant', 'lactating']
life_stage_arr= ['< 6 mo', '< 12 mo', '1 to 3 y', '4 to 8 y', '9 to 13 y',
                       '14 to 18 y', '19 to 30 y', '31 to 50 y', '51 to 70 y',
                       '> 70 y']
active_level_dict = {'sedentary': 'sedentary',
                     'moderately active': 'moderately_active',
                     'active': 'active'}

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
                dcc.Input(placeholder='Enter age...',
                          id='profile-age-input',
                          type='text'),
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
                dbc.Label("Activity Level:"),
                dcc.Dropdown(
                    id='active-lvl-dropdown',
                    options=[{'label': k, 'value': v} for k,v in active_level_dict.items()]
                )
            ])
        ], width=6)
    ])
], id="user-prof-layout", style={'display': 'block'})

