from xml.sax.handler import property_interning_dict
import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
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


dash.register_page(__name__)


stocks_trans_to_clientnames6 = pd.read_csv(
    './data/version_features_data.csv')



fig = px.line(stocks_trans_to_clientnames6, x="date", y=stocks_trans_to_clientnames6.columns,
              hover_data={"date": "|%B %d, %Y"},
              title='custom tick labels')

fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
fig.add_vline(x='2018-07-16', line_width=3,
              line_dash="dash", line_color="green")
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


#checklist_option = stocks_trans_to_clientnames6.columns.tolist()[1:]
checklist_option = ['Client_A', 'Client_B', 'Client_C', 'Client_D', 'Client_E']
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




