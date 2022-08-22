import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px


# dash.register_page(__name__)

dash.register_page(__name__)


#########


#######

card_content = dbc.Card(
    [
        dbc.CardHeader("Card header"),
        dbc.CardBody(
            [
                html.H5("Card title", className="card-title"),
                html.P(
                    "This is some card content that we'll reuse",
                    className="card-text",),
            ],),
    ])

body_app = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="primary", inverse=True)),
                dbc.Col(
                    dbc.Card(card_content, color="secondary", inverse=True)
                ),
                dbc.Col(dbc.Card(card_content, color="info", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="success", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="danger", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="light")),
                dbc.Col(dbc.Card(card_content, color="dark", inverse=True)),
            ]
        ),
    ]
)


layout = html.Div(id='parent', children=[body_app])
