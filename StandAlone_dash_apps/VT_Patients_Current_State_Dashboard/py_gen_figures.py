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




# def data_dict():
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
for ticker in ['AMZN', 'NFLX', 'SBUX', 'DIS', 'MSFT', 'TSLA']:
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
    # return dict_income, dict_balsheet, dict_financials, dict_q_income, dict_q_balsheet, dict_q_financials, dict_price, dict_overview


def update_figure(st):
    THEME = 'ggplot2'
    MARGIN = dict(t=10, b=20, l=10, r=10)

    fig_rev = px.bar(dict_income[st]['Revenue'], y='Revenue', text_auto='.3s',)
    fig_rev.update_layout(template=THEME, margin=MARGIN)
    fig_rev.update_traces(textposition="outside", cliponaxis=False, marker_color='mediumaquamarine')

    fig_net_inc = px.bar(dict_income[st]['Net Income'], y='Net Income', text_auto='.3s', )
    fig_net_inc.update_layout(template=THEME, margin=MARGIN)
    fig_net_inc.update_traces(marker_color='skyblue', textposition="outside", cliponaxis=True)

    fig_debt = px.bar(dict_balsheet[st]['Total Liabilities'], y='Total Liabilities', text_auto='.3s', )
    fig_debt.update_layout(template=THEME, margin=MARGIN)
    fig_debt.update_traces(marker_color='peachpuff',  textposition="outside", cliponaxis=False)

    fig_fcf = px.bar(dict_balsheet[st]['Cash On Hand'], y='Cash On Hand', text_auto='.3s', )
    fig_fcf.update_layout(template=THEME, margin=MARGIN)
    fig_fcf.update_traces(marker_color='darkturquoise', textposition="outside", cliponaxis=False)

    fig_shares = px.bar(dict_income[st]['Shares Outstanding'], y='Shares Outstanding', text_auto='.3s', )
    fig_shares.update_layout(template=THEME, margin=MARGIN)
    fig_shares.update_traces(marker_color='lightsalmon',  textposition="outside", cliponaxis=False)

    fig_netprof = px.bar(dict_financials[st]['Net Profit Margin'], y='Net Profit Margin', text_auto='.2f')
    fig_netprof.update_layout(template=THEME, margin=MARGIN)
    fig_netprof.update_traces(marker_color='darkkhaki', textposition="outside", cliponaxis=False)

    fig_pricehist = px.line(dict_price[st], y='Close')
    fig_pricehist.update_layout(template=THEME, margin=MARGIN)
    fig_pricehist.update_traces(line_color='royalblue', line_width=3, )

    sec = 'Sector: ' + dict_overview[st]['sector'].iloc[0]
    ind = 'Industry: ' + dict_overview[st]['industry'].iloc[0]
    pe = 'P/E Ratio: ' + str(dict_overview[st]['p/e'].iloc[0])
    comp = 'Company Name: ' + dict_overview[st]['company'].iloc[0]
    pri = 'Latest Price: ' + str(dict_overview[st]['price'].iloc[0])

    return fig_rev, fig_netprof, fig_shares, fig_net_inc, fig_debt, fig_fcf, fig_pricehist, sec, ind, pe, comp, pri



def fig_rev(tickerName):
    """    # 'User Groth' dcc.Graph(id='debtchart',figure=fig_list[0]=fig_rev

    """    
    THEME = 'ggplot2'

    MARGIN = dict(t=10, b=20, l=10, r=10)

    fig_rev = px.bar(dict_income[tickerName]['Revenue'], y='Revenue', text_auto='.3s', )
    fig_rev.update_layout(xaxis_title="Date", yaxis_title="Number of Users")
    fig_rev.update_layout(template=THEME, margin=MARGIN)
    fig_rev.update_traces(textposition="outside", cliponaxis=False, marker_color='mediumaquamarine')
    return fig_rev


def fig_net_inc(tickerName):
    """# this is the "ebitdachart" = header=internal(Compliance)"""
    THEME = 'ggplot2'
    MARGIN = dict(t=10, b=20, l=10, r=10)
    fig_net_inc = px.bar(dict_income[tickerName]['Net Income'], y='Net Income', text_auto='.3s', )
    fig_net_inc.update_layout(template=THEME, margin=MARGIN)
    fig_net_inc.update_layout(xaxis_title="Date", yaxis_title="%")
    fig_net_inc.update_traces(marker_color='skyblue', textposition="outside", cliponaxis=True)
    return fig_net_inc

def fig_debt(tickerName):
    """
    #  html.H5('Patiants Satisfaction', className='text-center'),  dcc.Graph(id='shareschart',figure=fig_list[4
    """

    THEME = 'ggplot2'
    MARGIN = dict(t=10, b=20, l=10, r=10)
    fig_debt = px.bar(dict_balsheet[tickerName]['Total Liabilities'], y='Total Liabilities', text_auto='.3s', )
    fig_debt.update_layout(template=THEME, margin=MARGIN)
    fig_debt.update_layout(xaxis_title="Date", yaxis_title="score")
    fig_debt.update_traces(marker_color='peachpuff',  textposition="outside", cliponaxis=False)
    return fig_debt

def fig_fcf(tickerName):
    """    # html.H5('Number of Remiders Sent', className='text-center'), dcc.Graph(id='freecashchart',figure=freecashchart
    """
    THEME = 'ggplot2'
    MARGIN = dict(t=10, b=20, l=10, r=10)
    fig_fcf = px.bar(dict_balsheet[tickerName]['Cash On Hand'], y='Cash On Hand', text_auto='.3s', )

    fig_fcf.update_layout(xaxis_title="Date", yaxis_title="Total")

    fig_fcf.update_layout(template=THEME, margin=MARGIN)
    fig_fcf.update_traces(marker_color='darkturquoise', textposition="outside", cliponaxis=False)
    return fig_fcf


def fig_shares(tickerName):
    """ html.H5('Number of Forms Sent', className='text-center'), dcc.Graph(id='netprofitmargchart',netprofitmargchart = fig_netprof = figure=fig_list[2]
    """

    THEME = 'ggplot2'

    MARGIN = dict(t=10, b=20, l=10, r=10)
    fig_shares = px.bar(dict_income[tickerName]['Shares Outstanding'], y='Shares Outstanding', text_auto='.3s',)
    fig_shares.update_layout(template=THEME, margin=MARGIN)
    fig_shares.update_layout(xaxis_title="Date", yaxis_title="Total")
    fig_shares.update_traces(marker_color='lightsalmon',  textposition="outside", cliponaxis=False)

    return fig_shares

def fig_netprof(tickerName):
    """
    #  html.H5('Staff-to-Patient Ratio', className='text-center'),            dcc.Graph(id='revenuechart',figure=netprofitmargchart, style={'height': 350}),

    """
    THEME = 'ggplot2'
    MARGIN = dict(t=10, b=20, l=10, r=10)
    fig_netprof = px.bar(dict_financials[tickerName]['Net Profit Margin'], y='Net Profit Margin', text_auto='.2f')
    fig_netprof.update_layout(template=THEME, margin=MARGIN)
    fig_netprof.update_layout(xaxis_title="Date", yaxis_title="Total")
    fig_netprof.update_traces(marker_color='darkkhaki', textposition="outside", cliponaxis=False)
    return fig_netprof


def fig_pricehist(tickerName):
    """  
    html.H5('2Y New-Patients', className='text-center p-1')
    pricechart = fig_pricehist

    dcc.Graph(id='pricechart',figure=fig_list[5])
    """
    THEME = 'ggplot2'
    MARGIN = dict(t=10, b=20, l=10, r=10)
    fig_pricehist = px.line(dict_price[tickerName], y='Close')
    fig_pricehist.update_layout(template=THEME, margin=MARGIN)
    fig_pricehist.update_layout(xaxis_title="TimeSeries", yaxis_title="TotalNewPatients")
    fig_pricehist.update_traces(line_color='royalblue', line_width=3, )
    return fig_pricehist




