# Import necessary libraries
import dash
from dash import html
import dash_bootstrap_components as dbc

import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback
import plotly.express as px


import pandas as pd

# Plot # 5 :

# Name : UserActivity on VersionReleaseTimeline.

# Importing required modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

# Reading in the data


# app = Dash(__name__)
# df = pd.read_csv(
# 'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
df = pd.read_csv('./data/fakedata_lifexpec_india.csv')

layout = html.Div([
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    ),
    dcc.Graph(id='graph-with-slider'),

])




@ callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    df = pd.read_csv('./data/fakedata_lifexpec_india.csv')

    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


# if __name__ == '__main__':
#     app.run_server(debug=True)
