from dash import Dash, dcc, dash_table, Input, Output
import dash

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


#app = Dash(external_stylesheets=[dbc.themes.FLATLY],)
app = dash.Dash(__name__)


df_Dashboard_data = pd.read_csv(
    '/Users/sagilevinas/Desktop/VT_mar22/projects/devop/vt-architecture-plus-modernization-planning/jupyter/by_subject/Analytics/df_Dashboard_data.csv')
columns_zigi = ['date', 'clientName', 'n_AdminTeam', 'n_medTeam',
                'n_Patients', 'n_activeForms', 'n_CompletedForms', 'totalUsers']

latestdate_group_df = df_Dashboard_data.groupby(
    ['date']).get_group(('2020-12-01'))

latestToatalUsers = latestdate_group_df['totalUsers'].sum()

latestToatalPatients = latestdate_group_df['n_Patients'].sum()

latestToatalAdmin = latestdate_group_df['n_AdminTeam'].sum()

latestToatalMed = latestdate_group_df['n_medTeam'].sum()

latestToatalActiveForms = latestdate_group_df['n_activeForms'].sum()

latestToatalCompletedForms = latestdate_group_df['n_CompletedForms'].sum()

latestToatal_CompLiance = (
    (latestToatalCompletedForms/latestToatalActiveForms))

COVID_IMG = "/Users/sagilevinas/Desktop/VT_mar22/projects/devop/vt-architecture-plus-modernization-planning/jupyter/images/logo-visiontree.png"


#COVID_IMG = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fbigredmarkets.com%2Fwp-content%2Fuploads%2F2020%2F03%2FCovid-19.png&f=1&nofb=1"


url = "https://api.covid19api.com/summary"
response_world = requests.request("GET", url)
df_countries = pd.DataFrame(response_world.json()['Countries'])
df_global = pd.DataFrame(response_world.json()['Global'], index=[0])
df_last_updated = response_world.json()['Date']

#confirmed = df_global['TotalConfirmed'][0]
confirmed = latestToatalUsers


#newconfirmed = df_global['NewConfirmed'][0]
TotalCareTeam = latestToatalAdmin + latestToatalMed
TotalPatients = latestToatalPatients

deaths = df_global['TotalDeaths'][0]

newdeaths = df_global['NewDeaths'][0]
recovered = df_global['TotalRecovered'][0]
newrecovered = df_global['NewRecovered'][0]


#code_mapping = pd.DataFrame(data)

#df_world_f=pd.merge(df_countries[['Country','TotalConfirmed','TotalDeaths','TotalRecovered','CountryCode']],code_mapping, left_on = 'CountryCode',right_on = 'alpha-2',how = 'inner')
df_world_f = ""


#################################   Functions for creating Plotly graphs and data card contents ################
def world_map(df):
    # fig = px.choropleth(df, locations="iso_alpha", color = "TotalConfirmed",
    #                     hover_name= "Country",
    #                     hover_data = ['TotalConfirmed','TotalDeaths','TotalRecovered'],
    #                     projection="orthographic",
    #                     color_continuous_scale=px.colors.sequential.Plasma)

    # fig.update_layout(margin = dict(l=4,r=4,t=4,b=4))

    #labels = ['AndersonClinic','BNI','Hospital_A','NeuroGen']
    #values = [4500, 2500, 1053, 500]

    #fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    fig = px.bar(df_Dashboard_data, x='date', y='totalUsers', color='clientName', barmode='group', text_auto='.2s',
                 title="Total User Breakdown by Client")
    fig.update_layout(margin=dict(l=20, r=20, t=35, b=20),
                      paper_bgcolor="LightSteelBlue",)
    # fig.update_layout(width=int(width))

    return fig
    # fig.show()

    return fig

#


def data_for_cases(header, latestToatalUsers, TotalCareTeam):
    card_content = [
        dbc.CardHeader(header),

        dbc.CardBody(
            [
                dcc.Markdown(dangerously_allow_html=True,
                             children=["{0} <br><sub>+{1}</sub></br>".format(latestToatalUsers, TotalCareTeam)])


            ]

        )
    ]

    return card_content

############################################ body of the dashboard ###########################


body_app = dbc.Container([

    #dbc.Row( html.Marquee("USA, India and Brazil are top 3 countries in terms of confirmed cases"), style = {'color':'green'}),

    dbc.Row([
        dbc.Col(dbc.Card(data_for_cases("TotalUsers", f'{latestToatalUsers:,}', f'{TotalCareTeam:,}'), color='primary', style={
                'text-align': 'center'}, inverse=True), xs=12, sm=12, md=4, lg=4, xl=4, style={'padding': '12px 12px 12px 12px'}),
        dbc.Col(dbc.Card(data_for_cases("TotalPatients", f'{TotalPatients:,}', f'{newrecovered:,}'), color='success', style={
                'text-align': 'center'}, inverse=True), xs=12, sm=12, md=4, lg=4, xl=4, style={'padding': '12px 12px 12px 12px'}),
        dbc.Col(dbc.Card(data_for_cases("Compliance", f'{latestToatal_CompLiance :,}', f'{newdeaths:,}'), color='danger', style={'text-align': 'center'}, inverse=True), xs=12, sm=12, md=4, lg=4, xl=4, style={'padding': '12px 12px 12px 12px'})]),

    html.Br(),
    html.Br(),

    dbc.Row(dbc.Col([html.Div(html.H4('VisionTree High View'),  style={
            'textAlign': 'center', 'fontWeight': 'bold', 'family': 'georgia', 'width': '100%'})])),

    html.Br(),
    html.Br(),

    dbc.Row(dbc.Col(dcc.Graph(id='pie-chart', figure=world_map(df_world_f)),
            style={'height': '450px'}, xs=12, sm=12, md=8, lg=8, xl=8)),

    dbc.Row(
        dbc.Col([
                html.Div([
                         dcc.Dropdown(id='table-dropdown', options=[{'label': i, 'value': i} for i in np.append(['All'], df_Dashboard_data['date'].unique(
                         ))], value='All',  placeholder='Select the country', style={'width': '100%', 'display': 'inline-block'})
                         ]),
                html.Div(id='df-table-output',
                         style={'height': '450px', 'text-align': 'center'})
                ]
                )
    )]
)

############################## navigation bar ################################

navbar = dbc.Navbar(id='navbar', children=[


    html.A(
        dbc.Row([
            dbc.Col(html.Img(src=COVID_IMG, height="70px")),
            dbc.Col(
                dbc.NavbarBrand("VisionTree Live Tracker", style={'color': 'black', 'fontSize': '25px', 'fontFamily': 'Times New Roman'}
                                )

            )


        ], align="center",
            # no_gutters = True
        ),
        href='/'
    ),

    dbc.Row(
        [
            dbc.Col(
                # dbc.Button(id = 'button', children = "Click Me!", color = "primary"),
                dbc.Button(id='button', children="Support Us",
                           color="primary", className='ml-auto', href='/')

            )
        ],
        # add a top margin to make things look nice when the navbar
        # isn't expanded (mt-3) remove the margin on medium or
        # larger screens (mt-md-0) when the navbar is expanded.
        # keep button and search box on same row (flex-nowrap).
        # align everything on the right with left margin (ms-auto).
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    )
    # dbc.Button(id = 'button', children = "Support Us", color = "primary", className = 'ml-auto', href = '/')


])


app.layout = html.Div(id='parent', children=[navbar, body_app])

#################################### Callback for adding interactivity to the dashboard #######################


@app.callback(Output(component_id='df-table-output', component_property='children'),
              [Input(component_id='table-dropdown', component_property='value')])
def update_table(date):
    if date == 'All':
        #df_final = df_countries
        df_final = df_Dashboard_data
    else:
        #df_final = df_countries.loc[df_countries['Country'] == '{}'.format(country)]
        df_final = df_Dashboard_data.loc[df_Dashboard_data['date'] == '{}'.format(
            date)]

    return dash_table.DataTable(
        # data = df_final[['Country','TotalConfirmed','TotalRecovered','TotalDeaths']].to_dict('records'),
        # columns = [{'id':c , 'name':c} for c in df_final[['Country','TotalConfirmed','TotalRecovered','TotalDeaths']].columns],
        data=df_final[['date', 'clientName', 'n_AdminTeam', 'n_medTeam', 'n_Patients',
                       'n_activeForms', 'n_CompletedForms', 'totalUsers']].to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df_final[['date', 'clientName', 'n_AdminTeam',
                                                         'n_medTeam', 'n_Patients', 'n_activeForms', 'n_CompletedForms', 'totalUsers']].columns],
        fixed_rows={'headers': True},

        sort_action='native',

        style_table={
            'maxHeight': '450px'
        },

        style_header={'backgroundColor': 'rgb(224,224,224)',
                      'fontWeight': 'bold',
                      'border': '4px solid white',
                      'fontSize': '12px'
                      },

        style_data_conditional=[

            {
                'if': {'row_index': 'odd',
                       # 'column_id': 'ratio',
                       },
                'backgroundColor': 'rgb(240,240,240)',
                'fontSize': '12px',
            },

            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(255, 255, 255)',
                'fontSize': '12px',

            }

        ],

        style_cell={
            'textAlign': 'center',
            'fontFamily': 'Times New Roman',
            'border': '4px solid white',
            'width': '10%',
            # 'whiteSpace':'normal',
            # 'overflow':'hidden',
            'textOverflow': 'ellipsis',



        }

        # style_data

    )


if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server(mode='external')

    # app.run_server(mode='jupyterlab')
    #app.run_server(debug=True, port=8877)
