import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

from Dashboard.utils.Shiny_utils import (rdi_nutrients, rdi_modelnames_arr, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

food_to_id_dict, food_names_arr, food_ids_arr = make_food_to_id_dict()


make_meal_layout=dbc.Container([
    dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="cnf-vs-rdi-one-elements"
                ),
                dcc.Graph(
                    id="cnf-vs-rdi-one-vitamins"
                ),
                dcc.Graph(
                    id="cnf-vs-rdi-one-macro"
                ),

            ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label(
                    "Enter age and select gender or pregnant/lactating"
            ),
            dcc.Input(
                id="age-input", type="number", value='30',
                debounce=True
            ),
            dcc.RadioItems(
                options=[
                    {'label': 'male', 'value': 'Males'},
                    {'label': 'female', 'value': 'Females'},
                    {'label': 'pregnant', 'value': 'Pregnancy'},
                    {'label': 'lactating', 'value': 'Lactation' }
                ],
                value='Females'
            ),
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            #todo: show warnings if over RDI and display red if over upper RDI
            html.Label(
                "Selected Ingredients"
            ),
            DataTable( # ingredient, amt, units
                id='cumul-ingreds-table',
                data=[],
                editable=True,
                style_cell={'textAlign': 'left'},
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)'
                }],
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                },
            ),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label(
                "1. Choose Ingredient"
            ),
            dcc.Input(
                id="search-ingredient",
                list="food_names", placeholder='Enter food name',
                debounce=True,
                style={'width': '80%'}
            ),
            html.Datalist(
                id="food_names", children=[
                    html.Option(value=food) for food in food_names_arr
                ]
            ),
            html.Button(
                "Search Ingredient", id='search-ingredient-btn'
            ),
        ], width=8),
        dbc.Col([

            html.Label(
                "2. Amount Units"
            ),
            dcc.Dropdown(
                id="units-dropdown",
                ),
            html.Br(),
            html.Label(
                "3. Quantity"
            ),
            dcc.Input(
                id="numerical-amount", type="number",
            ),
            html.Br(),
            html.Button(
                "Update Nutrient Table", id="update-nut-table-btn"
            ),

        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            html.Button(
                "Add to Recipe", id='add-ingredient', n_clicks=0
            ),
            html.Button(
                "Remove Ingredient", id="remove-ingredient", n_clicks=0
            ),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            DataTable(
                id="cnf-totals-table",
                data=[],
                editable=True,
                style_cell_conditional=[{
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['Name']
                ],
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)'
                }],
                style_header={
                    'backgroundColor': 'rgb(230,230,230)',
                    'fontWeight': 'bold'
                },
            )
        ], width=12)
    ]),
    # this is where different pages go
    dbc.Row([
        dbc.Col([
            html.Div(
                id="data-layout"
            )
        ], width=12)
    ])

], id="make-meal-layout", style={'display': 'block'}

)