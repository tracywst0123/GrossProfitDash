import pandas as pd
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
from gross_profit_dash_app.data_config import APPS, TEAMS, TEAM_APPS, YEAR_START, YEAR_TAR
from gross_profit_dash_app.dash_utils import get_app_fig, data_loader, get_selector_graph_combo, get_apps_checklist, \
    quarter_target_table, get_currency_selector, get_table, get_team_selector, get_apps_options

def construct_html_children(init_data, authority_teams=TEAMS, app_list=APPS):
    q_d_table, q_date_str = get_table(init_data, teams=authority_teams, QuarterOrYear=True)
    y_d_table, y_date_str = get_table(init_data, teams=authority_teams, QuarterOrYear=False)
    children_list = [html.Br(), html.Br(), get_currency_selector(),
                     html.H5(children='季度目标'),
                     html.H5(id='q_table_id', children=q_date_str), q_d_table, html.Br(), html.Br(),
                     html.H5(children='年度目标'),
                     html.H5(id='y_table_id', children=q_date_str), y_d_table, html.Br(), html.Br()]

    children_list.extend([get_team_selector(teams_list=authority_teams, default_team=authority_teams[0]),
                          get_apps_checklist('apps_choice', default_team=authority_teams[0]), html.Br(), html.Br()])

    children_list.extend(get_selector_graph_combo(init_data, 'total',
                                                  day_range=30,
                                                  multiple_apps=True,
                                                  apps_list=TEAM_APPS.get(TEAMS[0])))

    for app_name in app_list:
        combo = get_selector_graph_combo(init_data, app_name, day_range=30)
        children_list.extend(combo)

    return children_list


def get_layout(data, authority_teams=TEAMS, app_list=APPS):
    return html.Div(children=[html.H2(children='Gross Profit Dashboard'),
                              html.Button('Update', id='update-button'),
                              html.Div(id='layout',
                                       children=construct_html_children(data,
                                                                        authority_teams=authority_teams,
                                                                        app_list=app_list)),
                              html.Div(id='hidden_data', style={'display': 'none'}, children=[data.to_json()])],
                    id='dash_container')


def init_dashboard(server, data=None, url_base='/dash/', authority_teams=TEAMS):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server, url_base_pathname=url_base)
    if not data:
        data = data_loader()

    if 'total' in authority_teams:
        app_list = TEAM_APPS.get('total')
    else:
        app_list = []
        for tt in TEAMS:
            app_list += tt

    dash_app.layout = get_layout(data, authority_teams=authority_teams, app_list=app_list)
    init_callbacks(dash_app, combo_team=authority_teams, app_list=app_list)

    return dash_app


def init_callbacks(app, combo=True, combo_team=TEAMS, app_list=APPS):

    @app.callback([Output('hidden_data', 'children')], [Input('update-button', 'n_clicks')])
    def update_data(n_clicks):
        new_data = data_loader()
        return [new_data.to_json()]

    if combo:
        @app.callback([Output('q_team_profit_table', 'data'), Output('q_table_id', 'children')],
                      [Input('currency', 'value'), Input('hidden_data', 'children')])
        def update_currency(value, jdata):
            if value == 'RMB':
                d_table, date_str = quarter_target_table(pd.read_json(jdata), rmb=True, teams=combo_team)
            else:
                d_table, date_str = quarter_target_table(pd.read_json(jdata), rmb=False, teams=combo_team)
            return d_table.to_dict('records'), date_str

        @app.callback([Output('y_team_profit_table', 'data'), Output('y_table_id', 'children')],
                      [Input('currency', 'value'), Input('hidden_data', 'children')])
        def update_currency(value, jdata):
            if value == 'RMB':
                d_table, date_str = quarter_target_table(pd.read_json(jdata), rmb=True, teams=combo_team,
                                                         start_date=YEAR_START, total_dates=365, team_tar=YEAR_TAR)
            else:
                d_table, date_str = quarter_target_table(pd.read_json(jdata), rmb=False, teams=combo_team,
                                                         start_date=YEAR_START, total_dates=365, team_tar=YEAR_TAR)
            return d_table.to_dict('records'), date_str

        @app.callback([Output('apps_choice', 'options')],
                      [Input('team_selector', 'value')])
        def update_apps_selection(selector_team):
            return [get_apps_options(default_team=selector_team)]

        @app.callback([Output('apps_choice', 'value')],
                      [Input('apps_choice', 'options')])
        def update_apps_selection(options):
            return [[dictionary.get('value') for dictionary in options]]

        @app.callback(Output('total', 'figure'), [Input('apps_choice', 'value'),
                                                  Input('total_date_range', 'value'),
                                                  Input('hidden_data', 'children')])
        def update_apps_selection(apps_list, day_range, jdata):
            return get_app_fig(pd.read_json(jdata), 'total', day_range=day_range, multiple_apps=True, apps_list=apps_list)

    if app_list:
        for app_name in app_list:
            @app.callback(Output(app_name, 'figure'),
                          [Input('{}_date_range'.format(app_name), 'value'), Input('hidden_data', 'children')],
                          State(app_name, 'id'))
            def update_date_range(value, jdata, app_name_id):
                return get_app_fig(pd.read_json(jdata), app_name_id, day_range=value)

