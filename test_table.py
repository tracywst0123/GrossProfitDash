import pandas as pd
import plotly
import datetime
import plotly.graph_objects as go
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import get_app_fig, data_loader, get_currency_selector, get_table, quarter_target_table

app = dash.Dash()

data = data_loader()


def app_layout():
    data = data_loader()
    d_table, date_str = get_table(data)
    return html.Div([html.H2(id='table_id', children=date_str), get_currency_selector(), d_table])


def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))


app.layout = serve_layout


if __name__ == '__main__':
    port = 8000
    app.run_server(debug=True, host='0.0.0.0', port=port)