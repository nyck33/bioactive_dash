import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable

from dash_utils.Shiny_utils import (rdi_nutrients, rdi_modelnames_arr, make_food_to_id_dict, get_unit_names,
                                         make_foodgroup_df, make_conversions_df, make_nutrients_df,
                                         get_conversions_multiplier, mult_nutrients_df)

food_to_id_dict, food_names_arr, food_ids_arr = make_food_to_id_dict()


controls_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Store(  # todo: hide dataframes as json
                id="hidden-conversions-df", storage_type='local'
            ),
            dcc.Store(
                id="hidden-nutrients-df", storage_type='session'
            ),
            dcc.Store(
                id="hidden-cumul-ingreds-df", storage_type='local'
            ),
            dcc.Store(
                id='hidden-total-nutrients-df', storage_type='session'

            ),
            dcc.Store(  # todo: trigger on selecting age and lifestage group
                id="hidden-rdi-df", storage_type='local'
            ),

        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            # todo: show warnings if over RDI and display red if over upper RDI
            html.Label("Enter age"),
            dcc.Input(
                id="age-input", type="number", value='30',
                debounce=True
            ),
            html.Br(),
            html.Label("Select gender"),
            dcc.RadioItems(
                options=[
                    {'label': 'male', 'value': 'Males'},
                    {'label': 'female', 'value': 'Females'},
                    {'label': 'pregnant', 'value': 'Pregnancy'},
                    {'label': 'lactating', 'value': 'Lactation'}
                ],
                value='Females'
            ),
            html.Br(),

            html.Label("1. Choose Ingredient"),
            dcc.Input(
                id="search-ingredient",
                list="food_names",
                placeholder='Enter food name',
                debounce=True,
                style={'width': '80%'}
            ),
            html.Datalist(
                id="food_names",
                children=[
                    html.Option(value=food) for food in food_names_arr
                ]
            ),
            dbc.Button(
                "Search Ingredient",
                id='search-ingredient-btn',
                color='primary'
            ),
            html.Br(),
            html.Label("2. Amount Units"),
            dcc.Dropdown(
                id="units-dropdown",
            ),
            html.Br(),
            html.Label("3. Quantity"),
            dcc.Input(
                id="numerical-amount",
                type="number",
            ),
            html.Br(),
            dbc.Button(
                "Update Nutrient Table",
                id="update-nut-table-btn",
                color='primary'
            ),
            html.Br(),
            html.Div(
                id='error-message'
            ),
            html.Br(),
            dbc.Button(
                "Add to Recipe",
                id='add-ingredient',
                color='success',
                n_clicks=0
            ),
            dbc.Button(
                "Remove Ingredient",
                id="remove-ingredient",
                color='danger',
                n_clicks=0
            ),
            dcc.RadioItems(
                id="radio-display-type",
                options=[
                    {'label': 'Nutrient Tables & RDI for ingredient', 'value': 'cnf-table'},
                    {'label': 'Nutrient Tables & RDI for all ingredients', 'value': 'cnf-totals-table'},
                ],
                value='cnf-table'
            )

        ], width=6),
        dbc.Col([
            html.Label(
                "Selected Ingredients"
            ),
            DataTable(  # ingredient, amt, units
                id='cumul-ingreds-table',
                data=[],
                editable=True,
                #row_selectable='single',
                row_deletable=True,
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
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(
                id="data-layout"
            )
        ], width=12)
    ])

], id="controls-layout", style={'display': 'block'},

)

# injected layouts
cnf_layout = dbc.Container([
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
            html.Div(
                id="chosen-food"  # shows full name in <H3>
            ),
            html.Div(
                id="test-out"
            ),
            html.Br(),
            DataTable(
                id="table-foodgroup-source",
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
            html.Div(
                html.H5("Conversions Multipliers")
            ),
            html.Br(),
            DataTable(
                id="conversions-table",
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
            html.Div(
                html.H5("Nutrients")
            ),
            html.Br(),
            DataTable(
                id="nutrients-table",
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
            ),
            html.Br(),
            html.Div(
                id='err-nutrients-table'
            ),
            html.Pre(
                id='ctx-msg'
            ),
        ], width=12)
    ])
], id='cnf-layout', style={'display': 'block'})

cnf_totals_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="cnf-vs-rdi-totals-elements"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-totals-vitamins"
            ),
            dcc.Graph(
                id="cnf-vs-rdi-totals-macro"
            ),

        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            DataTable(
                id="cnf-totals-table",
                data=[],
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
        ])
    ])
],id='cnf-totals-layout', style={'display': 'none'})

