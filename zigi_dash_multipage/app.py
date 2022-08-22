from dash import Dash, html, dcc
import dash
import time
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = html.Div(
    [
        html.Br(),
        html.H1('Multi-page app with Dash Pages',
                style={'textAlign': 'center', 'color': colors['text']}),

        html.Div(
            [html.Div(dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"]
                               ))
             for page in dash.page_registry.values()], style={'font-size': '25px',
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dash.page_container])

if __name__ == '__main__':
    app.run_server(debug=True, port=8333)
