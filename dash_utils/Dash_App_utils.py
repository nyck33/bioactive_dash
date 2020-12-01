"""
make dataframes from cnf here and import from other files

"""
import numpy as np
import os, re
from pathlib import Path
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

'''
url_elements = 'https://www.ncbi.nlm.nih.gov/books/NBK545442/table/appJ_tab3/?report=objectonly'
url_vitamins = 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t2/?report=objectonly'
url_macroNutrients = 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t4/?report=objectonly'
url_upper_vitamins = 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t7/?report=objectonly'
url_upper_elements = 'https://www.ncbi.nlm.nih.gov/books/NBK545442/table/appJ_tab9/?report=objectonly'
url_macroNutrients_DistRange = "https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t5/?report=objectonly"
'''
files_arr = os.listdir('/home/nobu/Desktop/1_comp4911/1_cnfdash/csv_nutrientsRDI')
# leave out .ipynb
csv_names_arr = [x for x in files_arr if os.path.splitext(x)[1]=='.csv']
#in-place sort
csv_names_arr.sort()
#replace underscore with spaces
table_names_arr = [x.replace("_", " ") for x in csv_names_arr]
# leave off .csv extension
table_names_arr = [os.path.splitext(x)[0] for x in table_names_arr]

def change_dir(target_dir):
    """
    target_dir example: 'csv_nutrientsRDI/'
    """
    p = Path(os.getcwd())
    os.chdir(p)  # .parent)
    #print(f"chdir'ed: {os.getcwd()}")
    os.chdir(target_dir)
    #curr = os.getcwd()

def return_to_dir():
    # change directories back to app directory
    p = Path(os.getcwd())
    os.chdir(p.parent)

def make_dataframes(csv_dir):
    #target_dir = csv_dir
    df_arr= []
    change_dir(csv_dir)

    filename = ''
    for i in range(len(csv_names_arr)):
        df = pd.read_csv(csv_names_arr[i])
        df_arr.append(df)

    # change directories back to app directory
    return_to_dir()

    return df_arr


def generate_table(dataframe, max_rows=30):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def make_table(df):

    return dash_table.DataTable(
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        #fixed_columns={'headers': True, 'data':1},
        style_table={'overflowX': 'auto'},
        columns=[{"name":i, "id": i} for i in df.columns],
        data = df.to_dict('records'),
    )


def make_figure(df, name):
    """
    make all units the same before plotting
    todo: scaling is issue as some have higher intakes on orders of magnitude
    """
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)
    # extract nums and change into numeric data type
    dfc = df.copy().astype(str)
    for i in range(1, len(dfc.columns)):
        dfc[dfc.columns[i]] = dfc[dfc.columns[i]].str.extract('(\d+[.]?\d*)', expand=False)  # replace(r'[^0-9]+','')
        if 'mg' in dfc.columns[i]:
            # val = pd.to_numeric(dfc[dfc.columns[i]], errors='coerce') * 1
            val = dfc[dfc.columns[i]].astype(float) * 1.
            dfc[dfc.columns[i]] = val
        elif '\u03BCg' in dfc.columns[i]:
            # val = pd.to_numeric(dfc[dfc.columns[i]], errors='coerce') / 1000.
            val = dfc[dfc.columns[i]].astype(float) / 1000.
            dfc[dfc.columns[i]] = val
        elif 'g' in dfc.columns[i]:
            val = dfc[dfc.columns[i]].astype(float) * 1000.
            dfc[dfc.columns[i]] = val

    # dfc = dfc.replace('NaN', 0)
    dfc.fillna(0, inplace=True)
    #print(f'{name}\ndfc')
    print(dfc.dtypes)

    # turn df into dict for plotting
    #dfc = df.copy
    #print(dfc.columns[0])
    df_idx = dfc.set_index('Life-Stage Group', inplace=False)
    df_dict_idx = df_idx.to_dict(orient='index')

    # https://dev.to/fronkan/stacked-and-grouped-bar-charts-using-plotly-python-a4p
    # make values lists, keys to list and zip for a dict of {key: list}
    row_names, nutrient_names = [], []
    values = []
    # vals for each row, lifestage group
    curr_vals = []
    count = 0
    for k, v in df_dict_idx.items():
        row_names.append(k)
        for nutrient_name, value in v.items():
            if count == 0:
                nutrient_names.append(nutrient_name)
            curr_vals.append(value)
        values.append(curr_vals)
        curr_vals = []
        count += 1

    # merge dictionaries
    # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python-taking-union-o

    row_vals = dict(zip(row_names, values))

    labels = {'labels': nutrient_names}

    data = {**row_vals, **labels}

    #prepare data for plotting
    plot_data = []
    count = 0
    for row in row_names:
        plot_data.append(go.Bar(
            name=row,
            x=data['labels'],
            y=data[row],
            offsetgroup=count,
        )
        )
        count += 1

    fig_names = {'percent': '% of daily energy',
                 'units': 'amts in mg'}

    fig_name = fig_names['units']
    if 'range' in name:
        fig_name = fig_names['percent']

    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=f'{name}',
            yaxis_title=fig_name
        )
    )
    #fig.show()
    return fig
