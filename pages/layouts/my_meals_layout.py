"""
Query for meals and ingreds in date range
Show one meal at a time
Return Datatable of meal_id, meal_type, date
Show Date Range RDI profile
"""
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
from flask_login import current_user
from datetime import date, datetime

today = datetime.today().strftime('%Y-%m-%d')
date_arr = today.split('-')
year = int(date_arr[0])
month = int(date_arr[1])
day = int(date_arr[2])

# up to a year ago
now = datetime.now()
last_year = now.year - 1
next_year = now.year + 1

my_meals_layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Select Date Range of Meals"),
            dcc.DatePickerRange(
                id='meal-dates-range',
                min_date_allowed=date(last_year, 1, 1),
                max_date_allowed=date(next_year, 12, 31),
                initial_visible_month=date(year, month, day),
                end_date=date(year, month, day)
            ),
            dbc.Button(
                "Get Meals for Dates",
                id='daterange-meals-btn',
                color='primary'
            ),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                id='daterange-meals-table-out'
                # also get radios
            ),
        ], width=12)
    ])
], id='my-meals-layout', style={'display': 'block'})

period_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                id='daterange-rdi-chart'
                # total nuts / rdi * num days
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                id='rdi-calendar-out'
                #todo: nice to have calendar with nutrient selectors
                # that show which days you miss RDI for that nutrient
                # color coded
            )
        ], width=12)
    ])
], id='period-layout', style={'display': 'block'})

per_selection_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                id='selections-rdi-chart-out'
                # output rdi chart for selected row from 'meal-table-out'
                # select one meal or all meals in a day
            ),
            html.Div(
                id='selections-ingreds-table-out'
                # make this selectable to output RDI chart for ingred,
                # to see which ingred should be substituted, on selection,
                # output alt ingred
            ),

        ], width=12)
    ])
], id="per-selection-layout", style={'display': 'none'})

alt_ingreds_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(
                id='ingred-rdi-chart-out'
                # output table for selected ingred above
            ),
            #####################################################################
            html.Div(
                id='alt-ingreds-table-out'
                # at same time as ingred-rdi-table, output table of alt ingreds
                # selectable to see rdi of each
            ),
            html.Div(
                id='rdi-chart-alt-ingred-out'
                # rdi chart for alt ingred selected above
            ),
        ], width=12)
    ])
], id='alt-ingreds-layout', style={'display': 'none'})