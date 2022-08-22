"""
A simple app demonstrating how to dynamically render tab content containing
dcc.Graph components to ensure graphs get sized correctly. We also show how
dcc.Store can be used to cache the results of an expensive graph generation
process so that switching tabs is fast.
"""
import time
import pandas as pd
import plotly.express as px


import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html, callback

#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__)

layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Dynamically rendered tab content"),
        html.Hr(),
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="line", tab_id="line"),
                dbc.Tab(label="Histograms", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="line",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "line":
            return dcc.Graph(figure=data["line"])
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"


@callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["line", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    # data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    fileloc = './data/fakedata_lifexpec_india.csv'

    dataset_fake_vtlife = pd.read_csv(fileloc)
    df = dataset_fake_vtlife
    # df = px.data.gapminder()  # replace with your own data source
    # mask = df.continent.isin(continent)

    mask = dataset_fake_vtlife.continent.isin(["Americas", "Oceania"])

    fig = px.line(df[mask], x="year", y="lifeExp", color='country')

    line = fig
    # line = go.Figure(
    #     data=[go.line(x=data[:, 0], y=data[:, 1], mode="markers")]
    # )
    data = df[mask]
    hist_1 = go.Figure(data=[go.Histogram(x=data['country'])])
    hist_2 = go.Figure(data=[go.Histogram(x=data['continent'])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"line": line, "hist_1": hist_1, "hist_2": hist_2}

