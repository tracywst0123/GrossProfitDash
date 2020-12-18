import pandas as pd
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from gross_profit_dash_app.data_config import APPS
from gross_profit_dash_app.dash_utils import get_app_fig, data_loader, get_selector_graph_combo, get_apps_checklist, \
    quarter_target_table, get_currency_selector, get_table, get_team_selector, get_apps_options


def construct_html_children(init_data, total_graph_app_list=APPS, app_list=APPS):
    d_table, date_str = get_table(init_data)
    graph_list = [html.H5(id='table_id', children=date_str), get_currency_selector(), d_table, html.Br(), html.Br()]
    graph_list.extend([get_team_selector(), get_apps_checklist('apps_choice', selector_team='total'), html.Br(), html.Br()])
    graph_list.extend(get_selector_graph_combo(init_data, 'total',
                                               day_range=30,
                                               multiple_apps=True,
                                               apps_list=total_graph_app_list))

    for app_name in app_list:
        combo = get_selector_graph_combo(init_data, app_name, day_range=30)
        graph_list.extend(combo)

    return graph_list


def get_layout(data):
    return html.Div(children=[html.H2(children='Gross Profit Dashboard'),
                              html.Button('Update', id='update-button'),
                              html.Div(children=construct_html_children(data), id='layout'),
                              html.Div(id='hidden_data', style={'display': 'none'}, children=[data.to_json()])],
                    id='dash_container')


def init_dashboard(server, data=None, url_base='/dash/'):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server, url_base_pathname=url_base)
    if not data:
        data = data_loader()
    dash_app.layout = get_layout(data)
    init_callbacks(dash_app)

    return dash_app


def init_callbacks(app):

    @app.callback([Output('hidden_data', 'children')], [Input('update-button', 'n_clicks')])
    def update_data(n_clicks):
        new_data = data_loader()
        return [new_data.to_json()]

    @app.callback([Output('team_profit_table', 'data'), Output('table_id', 'children')],
                  [Input('currency', 'value'), Input('hidden_data', 'children')])
    def update_currency(value, jdata):
        if value == 'RMB':
            d_table, date_str = quarter_target_table(pd.read_json(jdata), rmb=True)
        else:
            d_table, date_str = quarter_target_table(pd.read_json(jdata), rmb=False)
        return d_table.to_dict('records'), date_str

    @app.callback([Output('apps_choice', 'options')],
                  [Input('team_selector', 'value')])
    def update_apps_selection(selector_team):
        return [get_apps_options(selector_team=selector_team)]

    @app.callback([Output('apps_choice', 'value')],
                  [Input('apps_choice', 'options')])
    def update_apps_selection(options):
        return [[dictionary.get('value') for dictionary in options]]

    @app.callback(Output('total', 'figure'), [Input('apps_choice', 'value'),
                                              Input('total_date_range', 'value'),
                                              Input('hidden_data', 'children')])
    def update_apps_selection(apps_list, day_range, jdata):
        return get_app_fig(pd.read_json(jdata), 'total', day_range=day_range, multiple_apps=True, apps_list=apps_list)

    @app.callback(Output('Space_K', 'figure'),
                  [Input('Space_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Space_K', day_range=value)

    @app.callback(Output('PrivacyPowerPro_K', 'figure'),
                  [Input('PrivacyPowerPro_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'PrivacyPowerPro_K', day_range=value)

    @app.callback(Output('Optimizer_K', 'figure'),
                  [Input('Optimizer_K_date_range', 'value'),  Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Optimizer_K', day_range=value)

    @app.callback(Output('FastClear_K', 'figure'),
                  [Input('FastClear_K_date_range', 'value'),  Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'FastClear_K', day_range=value)

    @app.callback(Output('Normandy_K', 'figure'),
                  [Input('Normandy_K_date_range', 'value'),  Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Normandy_K', day_range=value)

    @app.callback(Output('500_K', 'figure'),
                  [Input('500_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), '500_K', day_range=value)

    @app.callback(Output('Cookie_K', 'figure'),
                  [Input('Cookie_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Cookie_K', day_range=value)

    @app.callback(Output('ColorPhone_K', 'figure'),
                  [Input('ColorPhone_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'ColorPhone_K', day_range=value)

    @app.callback(Output('DogRaise_K', 'figure'),
                  [Input('DogRaise_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'DogRaise_K', day_range=value)

    @app.callback(Output('Rat_K', 'figure'),
                  [Input('Rat_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Rat_K', day_range=value)

    @app.callback(Output('LuckyDog_K', 'figure'),
                  [Input('LuckyDog_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'LuckyDog_K', day_range=value)

    @app.callback(Output('Amber_K', 'figure'),
                  [Input('Amber_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Amber_K', day_range=value)

    @app.callback(Output('River_K', 'figure'),
                  [Input('River_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'River_K', day_range=value)

    @app.callback(Output('Walk_K', 'figure'),
                  [Input('Walk_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Walk_K', day_range=value)

    @app.callback(Output('RunFast_K', 'figure'),
                  [Input('RunFast_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'RunFast_K', day_range=value)

    @app.callback(Output('Mars_K', 'figure'),
                  [Input('Mars_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Mars_K', day_range=value)

    @app.callback(Output('Apollo_K', 'figure'),
                  [Input('Apollo_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Apollo_K', day_range=value)

    @app.callback(Output('Athena', 'figure'),
                  [Input('Athena_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Athena', day_range=value)

    @app.callback(Output('Poseidon_K', 'figure'),
                  [Input('Poseidon_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Poseidon_K', day_range=value)

    @app.callback(Output('Ares_K', 'figure'),
                  [Input('Ares_K_date_range', 'value'), Input('hidden_data', 'children')])
    def update_date_range(value, jdata):
        return get_app_fig(pd.read_json(jdata), 'Ares_K', day_range=value)