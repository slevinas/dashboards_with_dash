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

# print('lllllll')
# print(os.getcwd())
# print("file and directories in this dir:")
# for filedirName in os.listdir('./stockfinancials_overview/fin_statements'):
#     print(filedirName)

# app = JupyterDash(__name__, external_stylesheets=[dbc.themes.LUX])
# # app = JupyterDash(__name__, external_stylesheets=[dbc.themes.CYBORG]) ## switch to a dark theme!
app = Dash(__name__, external_stylesheets=[
           dbc.themes.CYBORG])  # switch to a dark theme!

# d = pd.DataFrame(stocks)
# dd_labels = [{'label': d[0].unique()[i], 'value': d[0].unique()[i]}
#              for i in range(d[0].unique().shape[0])]
stocks = ['AMZN','NFLX', 'SBUX', 'DIS', 'MSFT', 'TSLA']

dd_labels = [{'label':i, 'value':i} for i in stocks]
dd_labels


# READ THE DATA
stocks = ['AMZN', 'NFLX', 'SBUX', 'DIS', 'MSFT', 'TSLA']
dict_income = {}
dict_balsheet = {}
dict_financials = {}
dict_q_income = {}
dict_q_balsheet = {}
dict_q_financials = {}
dict_price = {}
dict_overview = {}
for ticker in stocks:
    dict_balsheet[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_balsheet_{ticker}.csv', index_col='Date')
    dict_income[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_income_{ticker}.csv', index_col='Date')
    dict_financials[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_financials_{ticker}.csv', index_col='Date')
    dict_q_balsheet[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_q_balsheet_{ticker}.csv', index_col='Date')
    dict_q_income[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_q_income_{ticker}.csv', index_col='Date')
    dict_q_financials[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_q_financials_{ticker}.csv', index_col='Date')
    dict_price[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_price_{ticker}.csv', index_col='Date')
    dict_overview[ticker] = pd.read_csv(
        f'./stockfinancials_overview/fin_statements/dict_overview_{ticker}.csv')


firstpage = [
    dbc.Row([
        dbc.Col([
            html.H3('FINANCIAL ASSISTANT DASHBOARD',
                    className='text-center mb-3 p-3'),
            html.Hr(),
        ],
            width={'size': 12, 'offset': 0, 'order': 0}),
    ]),
    dbc.Row([
        dbc.Col([
            html.H6('Select the stock you want to look into:',
                    className='text-center mb-2 p-1'),
            dcc.Dropdown(
                id='stock-dropdown',
                options=dd_labels,
                value=dd_labels[0]['label'],
                clearable=False,
            ),
            html.Div(id='comp', className='text-center mt-3 p-2'),
            html.Div(id='pri', className='text-center p-2'),
            html.Div(id='sec', className='text-center p-2'),
            html.Div(id='ind', className='text-center p-2'),
            html.Div(id='p/e', className='text-center p-2'),

        ],
            width={'size': 4, 'offset': 0, 'order': 0}),

        dbc.Col([
            html.H5('2Y Price History', className='text-center p-1'),
            dcc.Graph(id='pricechart', style={'height': 400}),
        ],
            width={'size': 8, 'offset': 0, 'order': 0}),
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('Revenue', className='text-center'),
            html.H6('Millions of $', className='text-center font-italic'),
            dcc.Graph(id='revenuechart', style={'height': 350}),
            html.H5('Net Profit Margin', className='text-center'),
            html.H6('%', className='text-center font-italic'),
            dcc.Graph(id='netprofitmargchart', style={'height': 350}),
        ],
            width={'size': 4, 'offset': 0, 'order': 0}),
        dbc.Col([
            html.H5('Net Income', className='text-center'),
            html.H6('Millions of $', className='text-center font-italic'),
            dcc.Graph(id='ebitdachart', style={'height': 350}),
            html.H5('Cash On Hand', className='text-center'),
            html.H6('Millions of $', className='text-center font-italic'),
            dcc.Graph(id='freecashchart', style={'height': 350}),
        ],
            width={'size': 4, 'offset': 0, 'order': 0}),
        dbc.Col([
            html.H5('Total Liabilities', className='text-center'),
            html.H6('Millions of $', className='text-center font-italic'),
            dcc.Graph(id='debtchart', style={'height': 350}),
            html.H5('Shares Outstanding', className='text-center'),
            html.H6('Millions', className='text-center font-italic'),
            dcc.Graph(id='shareschart', style={'height': 350}),
        ],
            width={'size': 4, 'offset': 0, 'order': 0}),
    ]),
]

app.layout = html.Div(id='page-content', children=firstpage, className='p-3')


@app.callback(
    [
        Output("revenuechart", "figure"), Output(
            "netprofitmargchart", "figure"), Output("shareschart", "figure"),
        Output("ebitdachart", "figure"), Output("debtchart",
                                                "figure"), Output("freecashchart", "figure"),
        Output("pricechart", "figure"), Output(
            "sec", "children"), Output("ind", "children"),
        Output("p/e", "children"), Output("comp",
                                          "children"), Output("pri", "children"),
    ],
    Input('stock-dropdown', 'value')
)
def update_figure(st):
    THEME = 'ggplot2'
    MARGIN = dict(t=10, b=20, l=10, r=10)

    fig_rev = px.bar(dict_income[st]['Revenue'], y='Revenue',
                     text_auto='.3s', hover_data={'Revenue': ':,.2d'})
    fig_rev.update_layout(template=THEME, margin=MARGIN)
    fig_rev.update_traces(textposition="outside",
                          cliponaxis=False, marker_color='mediumaquamarine')

    fig_net_inc = px.bar(dict_income[st]['Net Income'], y='Net Income',
                         text_auto='.3s', hover_data={'Net Income': ':,.2d'})
    fig_net_inc.update_layout(template=THEME, margin=MARGIN)
    fig_net_inc.update_traces(marker_color='skyblue',
                              textposition="outside", cliponaxis=True)

    fig_debt = px.bar(dict_balsheet[st]['Total Liabilities'], y='Total Liabilities',
                      text_auto='.3s', hover_data={'Total Liabilities': ':,.2d'})
    fig_debt.update_layout(template=THEME, margin=MARGIN)
    fig_debt.update_traces(marker_color='peachpuff',
                           textposition="outside", cliponaxis=False)

    fig_fcf = px.bar(dict_balsheet[st]['Cash On Hand'], y='Cash On Hand',
                     text_auto='.3s', hover_data={'Cash On Hand': ':,.2d'})
    fig_fcf.update_layout(template=THEME, margin=MARGIN)
    fig_fcf.update_traces(marker_color='darkturquoise',
                          textposition="outside", cliponaxis=False)

    fig_shares = px.bar(dict_income[st]['Shares Outstanding'], y='Shares Outstanding',
                        text_auto='.3s', hover_data={'Shares Outstanding': ':,.2d'})
    fig_shares.update_layout(template=THEME, margin=MARGIN)
    fig_shares.update_traces(marker_color='lightsalmon',
                             textposition="outside", cliponaxis=False)

    fig_netprof = px.bar(
        dict_financials[st]['Net Profit Margin'], y='Net Profit Margin', text_auto='.2f')
    fig_netprof.update_layout(template=THEME, margin=MARGIN)
    fig_netprof.update_traces(marker_color='darkkhaki',
                              textposition="outside", cliponaxis=False)

    fig_pricehist = px.line(dict_price[st], y='Close')
    fig_pricehist.update_layout(template=THEME, margin=MARGIN)
    fig_pricehist.update_traces(
        line_color='royalblue', line_width=3, hovertemplate='Close @ %{x}: $%{y}')

    sec = 'Sector: ' + dict_overview[st]['sector'].iloc[0]
    ind = 'Industry: ' + dict_overview[st]['industry'].iloc[0]
    pe = 'P/E Ratio: ' + str(dict_overview[st]['p/e'].iloc[0])
    comp = 'Company Name: ' + dict_overview[st]['company'].iloc[0]
    pri = 'Latest Price: ' + str(dict_overview[st]['price'].iloc[0])

    return fig_rev, fig_netprof, fig_shares, fig_net_inc, fig_debt, fig_fcf, fig_pricehist, sec, ind, pe, comp, pri


if __name__ == "__main__":
    app.run_server(debug=True, port=8333)
