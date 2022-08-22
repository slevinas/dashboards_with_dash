import plotly.figure_factory as ff
import pandas as pd
import os
# df = pd.DataFrame()
# df['date'] = ['2016-04-01', '2016-04-02', '2016-04-03']
# df['calories'] = [2200, 2100, 1500]
# df['sleep hours'] = [8, 7.5, 8.2]
# df['gym'] = [True, False, False]


import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback
import plotly.express as px


logfil_cloudwatch_lgsinsigh_results = './data/test_df10N.csv'
#df23 = pd.read_csv(logfile23, header=None)
df_friN = pd.read_csv(logfil_cloudwatch_lgsinsigh_results)
print("zigiiiiiiii")
# print(os.getcwd())
# print(df_friN.head())
dash.register_page(__name__)

layout = html.Div([
    html.Br(),
    html.H4('Mosts Used Queries'),
    dcc.Checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa", "Americas", "Oceania"],
        value=["Americas", "Oceania"],
        inline=True
    ),
    html.Br(),
    dcc.Graph(id="graph"),

])


@callback(
    Output("graph", "figure"),
    Input("checklist", "value"))
def update_line_chart(continents):
    logfil_cloudwatch_lgsinsigh_results = './data/test_df10N.csv'
    #df23 = pd.read_csv(logfile23, header=None)
    df_friN = pd.read_csv(logfil_cloudwatch_lgsinsigh_results)

    test_df10N = df_friN.head(10).copy()
    print(test_df10N)

    fig = ff.create_table(test_df10N.iloc[:, [0, -1]])
    fig.update_layout(
        autosize=False,
        width=1500,
        height=400,
    )

    return fig
