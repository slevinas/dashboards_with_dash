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
stocks_trans_to_clientnames6 = pd.read_csv('/Users/sagilevinas/Desktop/projects/my-repositiries/dashboars_withe_dash/multipage-dash-app/data/version_features_data.csv')

stocks_trans_to_clientnames6.info()



fig = px.line(stocks_trans_to_clientnames6, x="date", y=stocks_trans_to_clientnames6.columns,
              hover_data={"date": "|%B %d, %Y"},
              title='custom tick labels')

fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
fig.add_vline(x='2018-07-16', line_width=3, line_dash="dash", line_color="green")
# import plotly.express as px

# df = px.data.stocks(indexed=True)
# fig = px.line(df)

fig.add_hline(y=1, line_dash="dot",
              annotation_text="Jan 1, 2018 baseline", 
              annotation_position="bottom right")

fig.add_vrect(x0="2018-09-24", x1="2018-12-18", 
              annotation_text="Version_2.3", annotation_position="top right",
              fillcolor="green", opacity=0.25, line_width=0)

fig.add_vrect(x0="2018-12-18", x1="2019-04-08", 
              annotation_text="Version_2.4", annotation_position="top right",
              fillcolor="purple", opacity=0.25, line_width=0)

fig.add_vrect(x0="2019-04-08", x1=stocks_trans_to_clientnames6['date'].max(), 
              annotation_text="Version_2.5", annotation_position="top right",
              fillcolor="blue", opacity=0.25, line_width=0)


              

# app = Dash(__name__)
# df = pd.read_csv(
# 'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
# df = pd.read_csv('./data/fakedata_lifexpec_india.csv')

# layout = html.Div([
#     dcc.Slider(
#         df['year'].min(),
#         df['year'].max(),
#         step=None,
#         value=df['year'].min(),
#         marks={str(year): str(year) for year in df['year'].unique()},
#         id='year-slider'
#     ),
#     dcc.Graph(id='graph-with-slider'),

# ])


# @ callback(
#     Output('graph-with-slider', 'figure'),
#     Input('year-slider', 'value'))
# def update_figure(selected_year):
#     df = pd.read_csv('./data/fakedata_lifexpec_india.csv')

#     filtered_df = df[df.year == selected_year]

#     fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                      size="pop", color="continent", hover_name="country",
#                      log_x=True, size_max=55)

#     fig.update_layout(transition_duration=500)

#     return fig

# import plotly.graph_objects as go # or plotly.express as px
# fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# # fig.add_trace( ... )
# # fig.update_layout( ... )

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
checklist_option = stocks_trans_to_clientnames6.columns.tolist()
#app = dash.Dash()
layout = dbc.Container(html.Div(
    [
     html.Div(children=[
        html.Br(),
        html.Label('Checkboxes'),
        dcc.Checklist(checklist_option,
                      ['Client_A', 'Client_B'])]),
    dcc.Graph(figure=fig)
    ]
)
)
