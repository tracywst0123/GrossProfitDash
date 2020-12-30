import pandas as pd
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
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


def init_callbacks(app, combo=True, combo_team='all', applist=APPS):

    @app.callback([Output('hidden_data', 'children')], [Input('update-button', 'n_clicks')])
    def update_data(n_clicks):
        new_data = data_loader()
        return [new_data.to_json()]

    if combo:

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

    if applist:
        for app_name in applist:
            @app.callback(Output(app_name, 'figure'),
                        [Input('{}_date_range'.format(app_name), 'value'), Input('hidden_data', 'children')],
                        State(app_name, 'id'))
            def update_date_range(value, jdata, app_name_id):
                return get_app_fig(pd.read_json(jdata), app_name_id, day_range=value)

