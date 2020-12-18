# -*- coding: utf-8 -*-
"""
@author; Nobu Kim
"""
import json
import re
import pandas as pd
from dash import Dash, exceptions, no_update, callback_context
from dash.dependencies import Input, Output, State
from dash_utils.Dash_fun import apply_layout_with_auth
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table import DataTable
from mongoengine import connect

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql

nut_engine = create_engine("mysql+pymysql://root:tennis33@localhost/dashcnf?charset=utf8mb4")#, echo=True)

nut_table_names = nut_engine.table_names()

#nutrient names from the above

nut_names_arr = [nut_name.replace("_foods", "") for nut_name in nut_table_names
                    if 'user' not in nut_name]

