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
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
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
                dbc.Tab(label="Scatter", tab_id="scatter"),
                dbc.Tab(label="Histograms", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
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
        if active_tab == "scatter":
            return dcc.Graph(figure=data["scatter"])
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    # data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    fileloc = "~/Desktop/VT_mar22/projects/devop/vt-architecture-plus-modernization-planning/jupyter/by_subject/Analytics/dataset-fake-vtlife-exprctency.csv"

    dataset_fake_vtlife = pd.read_csv(fileloc)
    df = dataset_fake_vtlife
    # df = px.data.gapminder()  # replace with your own data source
    # mask = df.continent.isin(continent)

    mask = dataset_fake_vtlife.continent.isin(["Americas", "Oceania"])

    fig = px.line(df[mask], x="year", y="lifeExp", color='country')

    scatter = fig
    # scatter = go.Figure(
    #     data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    # )
    data = df[mask]
    hist_1 = go.Figure(data=[go.Histogram(x=data['country'])])
    hist_2 = go.Figure(data=[go.Histogram(x=data['continent'])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}


if __name__ == "__main__":
    app.run_server(debug=True, port=8333)


# """
# Dash port of Shiny faithful example:

# https://shiny.rstudio.com/gallery/faithful.html

# Note: the shiny version includes a slider for adjusting the bandwidth of the
# density approximation curve, which is not easily adjusted when using
# plotly.figure_factory.create_distplot, so it doesn't feature in this example.
# """
# import dash
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.figure_factory as ff
# from dash import Input, Output, dcc, html

# DATA = pd.read_csv("https://cdn.opensource.faculty.ai/old-faithful/data.csv")

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# dropdown = html.Div(
#     [
#         dbc.Label("Number of bins in histogram (approximate):"),
#         dcc.Dropdown(
#             id="dropdown",
#             options=[{"label": n, "value": n} for n in [10, 20, 35, 50]],
#             value=20,
#         ),
#     ]
# )

# checklist = html.Div(
#     [
#         dbc.Label("Extras:"),
#         dbc.Checklist(
#             id="checklist",
#             options=[
#                 {"label": "Show individual observations", "value": "show_ind"},
#                 {"label": "Show density estimate", "value": "show_dens"},
#             ],
#             value=[],
#             inline=True,
#         ),
#     ]
# )


# app.layout = dbc.Container(
#     [
#         html.H1("Old Faithful eruption data"),
#         html.Hr(),
#         dbc.Row(
#             [
#                 dbc.Col(dropdown),
#                 dbc.Col(checklist, width="auto", align="center"),
#             ]
#         ),
#         html.Br(),
#         dcc.Graph(id="graph"),
#     ]
# )


# @app.callback(
#     Output("graph", "figure"),
#     [Input("dropdown", "value"), Input("checklist", "value")],
# )
# def make_graph(dropdown_value, checklist_value):
#     bin_size = (DATA.eruptions.max() - DATA.eruptions.min()) / dropdown_value
#     fig = ff.create_distplot(
#         [DATA.eruptions],
#         ["Eruption duration"],
#         bin_size=bin_size,
#         show_curve="show_dens" in checklist_value,
#         show_rug="show_ind" in checklist_value,
#     )
#     fig["layout"].update(
#         {
#             "title": "Geyser eruption duration",
#             "showlegend": False,
#             "xaxis": {"title": "Duration (minutes)"},
#             "yaxis": {"title": "Density"},
#         }
#     )
#     return fig


# if __name__ == "__main__":
#     app.run_server(debug=True, port=8333)
