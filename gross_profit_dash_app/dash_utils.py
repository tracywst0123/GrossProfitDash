import pandas as pd
import datetime
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_table

from gross_profit_dash_app.data_config import Q_START, TABLE_COLS, RMBperDOLLAR, TEAMS, TEAM_APPS, TEAM_TAR


def quarter_target_table(data, rmb=False, q_start=Q_START):
    d_table = pd.DataFrame(columns=TABLE_COLS)
    data['profit'] = data['earnings'] - data['spend'] - data['pay']
    data = data[data['date'] >= q_start]

    dates = data.date.unique()
    dates_str = str(dates[0])[:10] + ' ~ ' + str(dates[-1])[:10]
    day_range = len(dates)

    if rmb:
        div_factor = 1
    else:
        div_factor = RMBperDOLLAR

    for team in TEAMS:
        apps = TEAM_APPS.get(team)
        data_team = data[data['app'].isin(apps)]

        day_revenue = data_team.earnings.sum()/day_range  # 平均日收入
        day_cost = (data_team.spend.sum() + data_team.pay.sum())/day_range  # 平均日消耗

        day_target = TEAM_TAR.get(team)              # 日均目标
        q_done = data_team.profit.sum()              # 已完成利润
        q_target = 92 * day_target                   # 季度目标
        day_done = q_done/day_range                  # 平均日利润
        day_diff = (day_target*day_range - q_done)/day_range  # 平均利润差
        q_todo = q_target - q_done                   # 剩余季度目标
        day_todo = q_todo/(92 - day_range)           # 剩余日目标

        last_day_data = data_team[data_team['date'] >= dates[-1]]
        last_day_revenue = last_day_data.earnings.sum()  # 昨日组收入
        last_day_cost = last_day_data.spend.sum() + last_day_data.pay.sum()  # 昨日组消耗

        values = [team]
        values.extend([int(v/div_factor) for v in [q_target, day_target, q_done, day_done, day_diff, q_todo, day_todo,
                                                   day_revenue, day_cost, last_day_revenue, last_day_cost]])
        d_table = d_table.append(pd.DataFrame([values], columns=TABLE_COLS))

    return d_table, dates_str


def get_table(data, rmb=False):
    dd_table, date_str = quarter_target_table(data, rmb=rmb)
    d_table = dash_table.DataTable(id='team_profit_table',
                                   columns=[{'id': c, 'name': c} for c in TABLE_COLS],
                                   data=dd_table.to_dict('records'),
                                   style_table={'width': '90%'},
                                   style_data_conditional=[
                                       {'if': {'filter_query': '{平均利润差} > 0', 'column_id': '平均利润差'},
                                        'color': 'tomato', 'fontWeight': 'bold'},
                                       {'if': {'filter_query': '{平均利润差} < 0', 'column_id': '平均利润差'},
                                        'color': 'green'},
                                       {'if': {'column_id': '剩余日目标'},
                                        'color': 'purple', 'fontWeight': 'bold'}])
    return d_table, date_str


def get_currency_selector():
    return dcc.RadioItems(id='currency',
                          options=[{'label': 'RMB', 'value': 'RMB'},
                                   {'label': 'Dollar', 'value': 'Dollar'}],
                          value='RMB')


def get_selector_graph_combo(data, app_name, day_range, multiple_apps=False, apps_list=None):

    return [get_time_selector(app_name),
            dcc.Graph(id=app_name, figure=get_app_fig(data,
                                                      app_name,
                                                      day_range,
                                                      multiple_apps=multiple_apps,
                                                      apps_list=apps_list))]


def init_date(day_range=30):
    d = datetime.date.today() - datetime.timedelta(days=day_range)
    return datetime.datetime(d.year, d.month, d.day)


def get_time_selector(app):
    return dcc.RadioItems(id=app + '_date_range',
                          options=[{'label': '30 天', 'value': 30},
                                   {'label': '60 天', 'value': 60},
                                   {'label': '90 天', 'value': 90}],
                          value=30)


def get_app_fig(data, app_name, day_range, multiple_apps=False, apps_list=None):
    if multiple_apps:
        data = data[(data['date'] > init_date(day_range=day_range)) & (data['app'].isin(apps_list))]
        data = data.groupby('date').sum()
        data = data.reset_index()
    else:
        data = data[(data['date'] > init_date(day_range=day_range)) & (data['app'] == app_name)]
    return draw_diverging_profit(data, app_name)


def draw_diverging_profit(data, name):
    x = data.date
    sum_xy = data.earnings - data.spend - data.pay
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=data.earnings, name='Profit'))
    fig.add_trace(go.Bar(x=x, y=-data.spend, name='Cost'))
    fig.add_trace(go.Scatter(x=x, y=sum_xy, mode='lines+markers', name='Gross'))
    fig.add_trace(go.Bar(x=x, y=-data.pay, name='Withdraw'))
    gross_profit = int(sum(data.earnings) - sum(data.spend) - sum(data.pay))
    fig.update_layout(barmode='relative',
                      title_text=name+'      = '+str(gross_profit))
    return fig


def get_team_selector(team='total'):
    return dcc.RadioItems(id='team_selector',
                          options=[{'label': 'total', 'value': 'total'},
                                   {'label': '010', 'value': '010'},
                                   {'label': '060', 'value': '060'},
                                   {'label': '075', 'value': '075'}],
                          value=team)


def get_apps_options(selector_team='total'):
    return [{'label': app, 'value': app} for app in TEAM_APPS.get(selector_team)]


def get_apps_checklist(checklist_id, selector_team='total'):
    return dcc.Checklist(id=checklist_id,
                         options=get_apps_options(selector_team),
                         value=TEAM_APPS.get(selector_team))


def data_loader(cost_path='/Users/tracy/PycharmProjects/GrossProfitDash/data/cost.csv',
                revenue_path='/Users/tracy/PycharmProjects/GrossProfitDash/data/revenue.csv',
                pay_path='/Users/tracy/PycharmProjects/GrossProfitDash/data/pay.csv'):
    cost = pd.read_csv(cost_path)
    cost['date'] = cost['date'].apply(pd.to_datetime)

    revenue = pd.read_csv(revenue_path)
    revenue['date'] = revenue['date'].apply(pd.to_datetime)

    pay = pd.read_csv(pay_path)
    pay['date'] = pay['date'].apply(pd.to_datetime)

    left = pd.merge(cost, revenue, on=['date', 'app'])
    data = pd.merge(left, pay, on=['date', 'app'], how='left').fillna(0)
    data = data[['date', 'app', 'spend', 'earnings', 'pay']]
    data = data.sort_values(by=['date'])

    return data


