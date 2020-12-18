import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


df = px.data.tips()
print(type(df))
print(df)
days = df.day.unique()

app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in days],
        value=days[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-chart"),
])


@app.callback(
    Output("bar-chart", "figure"), 
    [Input("dropdown", "value")])
def update_bar_chart(day):
    mask = df["day"] == day
    fig = px.bar(df[mask], x="sex", y="total_bill", 
                 color="smoker", barmode="group")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
