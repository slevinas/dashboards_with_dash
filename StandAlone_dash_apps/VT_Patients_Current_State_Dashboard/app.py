from dash import Dash, dcc, dash_table, Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html
import requests
import numpy as np
#from dash.dependencies import Input,Output
import plotly.graph_objects as go
import re
import os

from py_gen_figures import *

#based on source: https://medium.datadriveninvestor.com/visualizing-some-key-financial-metrics-for-your-stocks-f987ea37035e



# # app = JupyterDash(__name__, external_stylesheets=[dbc.themes.CYBORG]) ## switch to a dark theme!
app = Dash(__name__, external_stylesheets=[
           dbc.themes.CYBORG])  # switch to a dark theme!

# d = pd.DataFrame(stocks)
# dd_labels = [{'label': d[0].unique()[i], 'value': d[0].unique()[i]}
#              for i in range(d[0].unique().shape[0])]
stocks = ['AMZN', 'NFLX', 'SBUX', 'DIS', 'MSFT', 'TSLA']

dd_labels = [{'label': i, 'value': i} for i in stocks]

# print(dd_labels)
# [{'label': 'AMZN', 'value': 'AMZN'}, {'label': 'NFLX', 'value': 'NFLX'}, {'label': 'SBUX', 'value': 'SBUX'}, {'label': 'DIS', 'value': 'DIS'}, {'label': 'MSFT', 'value': 'MSFT'}, {'label': 'TSLA', 'value': 'TSLA'}]


THEME = 'ggplot2'
MARGIN = dict(t=50, b=30, l=25, r=25)


## using local imports for the figurs to make the app code more crearer and cleaner 
st = "AMZN"
fig_rev = fig_rev(st)
fig_net_inc = fig_net_inc(st)
fig_debt = fig_debt(st)
fig_fcf = fig_fcf(st)
fig_shares = fig_shares(st)
fig_netprof = fig_netprof(st)
fig_pricehist = fig_pricehist(st)
#print(type(fig_rev))



revenuechart = fig_rev
netprofitmargchart = fig_netprof
shareschart = fig_shares
ebitdachart = fig_net_inc
debtchart =  fig_debt
freecashchart =  fig_fcf
pricechart = fig_pricehist
sec = 'Sector: ' + dict_overview[st]['sector'].iloc[0]
ind = 'Industry: ' + dict_overview[st]['industry'].iloc[0]
pe = 'P/E Ratio: ' + str(dict_overview[st]['p/e'].iloc[0])
comp = 'Company Name: ' + dict_overview[st]['company'].iloc[0]
pri = 'Latest Price: ' + str(dict_overview[st]['price'].iloc[0])
fig_list = [fig_rev,fig_netprof, fig_shares,fig_net_inc,fig_debt,fig_pricehist,sec,ind,pe,comp,pri]


firstpage = [
    dbc.Row(
        [
        dbc.Col(
            [
            html.H3('VisionTree Current State DASHBOARD', className='text-center mb-3 p-3'),
            html.Hr(),
            ],  width={'size': 12, 'offset': 0, 'order': 0}
                ),
        ]   ),
   

    dbc.Row(
        [
        dbc.Col(
            [
            html.H6('Select the Company you want to look into:', className='text-center mb-2 p-1'),
            dcc.Dropdown(id='stock-dropdown', options=["Us_Oncolygy","SaintSomethingHospital"], value="CompanyName", clearable=False),
            html.Div(id='comp', className='text-center mt-3 p-2'),
            html.Div(id='pri', className='text-center p-2'),
            html.Div(id='sec', className='text-center p-2'),
            html.Div(id='ind', className='text-center p-2'),
            html.Div(id='p/e', className='text-center p-2'),
             ], width={'size': 4, 'offset': 0, 'order': 0}
                ),
        dbc.Col(
            [
            html.H5('2Y New-Patients', className='text-center p-1'),
            dcc.Graph(id='pricechart',figure=fig_list[5], style={'height': 400}),
             ], width={'size': 8, 'offset': 0, 'order': 0}
                ),
        ]   ),

     html.Br(),


    dbc.Row([
        dbc.Col([
            html.H5('Staff-to-Patient Ratio', className='text-center'),
            html.H6('nurse-to-patients', className='text-center font-italic'),
            dcc.Graph(id='revenuechart',figure=netprofitmargchart, style={'height': 350}),
            html.Br(),
            html.H5('Number of Forms Sent', className='text-center'),
            html.H6(':', className='text-center font-italic'),
            dcc.Graph(id='netprofitmargchart',figure=fig_list[2], style={'height': 350}),
        ],
            width={'size': 4, 'offset': 0, 'order': 0}),
        dbc.Col([
            html.H5('Compliance', className='text-center'),
            html.H6('as %', className='text-center font-italic'),
            dcc.Graph(id='ebitdachart',figure=ebitdachart, style={'height': 350}),
            html.Br(),
            html.H5('Number of Remiders Sent', className='text-center'),
            html.H6('in thousands', className='text-center font-italic'),
            dcc.Graph(id='freecashchart',figure=freecashchart, style={'height': 350}),
        ],
            width={'size': 4, 'offset': 0, 'order': 0}),
        dbc.Col([
            html.H5('User Groth', className='text-center'),
            html.H6('Millions of $', className='text-center font-italic'),
            dcc.Graph(id='debtchart',figure=fig_list[0], style={'height': 350}),
            html.Br(),
            html.H5('Patiants Satisfaction', className='text-center'),
            html.H6('rank', className='text-center font-italic'),
            
            dcc.Graph(id='shareschart',figure=fig_list[4], style={'height': 350}),
        ],
            width={'size': 4, 'offset': 0, 'order': 0}),
    ]),
]

app.layout = html.Div(id='page-content', children=firstpage, className='p-3')




if __name__ == "__main__":
    app.run_server(debug=True, port=8333)
