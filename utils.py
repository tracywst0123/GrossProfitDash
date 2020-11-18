import numpy as np
import pandas as pd
import datetime
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_table


RMBperDOLLAR = 6.7


APP_LIST = [('Space_K', 'com.oneapp.max.cleaner.booster.cn'),
            ('PrivacyPowerPro_K', 'com.oneapp.max.security.pro.cn'),
            ('Optimizer_K', 'com.oneapp.max.cn'),
            ('FastClear_K', 'com.boost.clean.coin.cn'),
            ('Normandy_K', 'com.normandy.booster.cn'),
            ('500_K', 'com.honeycomb.launcher.cn'),
            ('Cookie_K', 'com.emoticon.screen.home.launcher.cn'),
            ('ColorPhone_K', 'com.colorphone.smooth.dialer.cn'),
            ('DogRaise_K', 'com.dograise.richman.cn'),
            ('Rat_K', 'com.rat.countmoney.cn'),
            ('LuckyDog_K', 'com.fortunedog.cn'),
            ('Amber_K', 'com.diamond.coin.cn'),
            ('River_K', 'com.crazystone.coin.cn'),
            ('Walk_K', 'com.walk.sports.cn'),
            ('Mars_K', 'com.cyqxx.puzzle.idiom.cn'),
            ('Athena', '1503126294'),
            ('Apollo_K', 'com.yqs.cn'),
            ('Poseidon_K', 'com.lightyear.dccj')]

APPS = ['Space_K', 'PrivacyPowerPro_K', 'Optimizer_K', 'FastClear_K', 'Normandy_K', '500_K', 'Cookie_K',
        'ColorPhone_K', 'DogRaise_K', 'Rat_K', 'LuckyDog_K', 'Amber_K', 'River_K', 'Walk_K', 'Mars_K',
        'Athena', 'Apollo_K', 'Poseidon_K']

TEAM_APPS = {'总': ['Space_K', 'PrivacyPowerPro_K', 'Optimizer_K', 'FastClear_K', '500_K', 'Cookie_K',
                   'ColorPhone_K', 'DogRaise_K', 'Rat_K', 'LuckyDog_K', 'Amber_K', 'River', 'Walk_K',
                   'Mars_K', 'Athena', 'Apollo_K', 'Poseidon_K'],
             '010': ['Space_K', 'PrivacyPowerPro_K', 'Optimizer_K', 'FastClear_K', 'Amber_K', 'Walk_K', 'River_K'],
             '075': ['Mars_K', 'Athena', 'Apollo_K', 'Poseidon_K'],
             '060': ['500_K', 'Cookie_K', 'ColorPhone_K', 'DogRaise_K', 'Rat_K', 'LuckyDog_K'],
             '080': ['Normandy_K']}

TEAM_TAR = {'总': 80000*RMBperDOLLAR,
            '010': 40000*RMBperDOLLAR,
            '075': 20000*RMBperDOLLAR,
            '060': 20000*RMBperDOLLAR,
            '080': 5000*RMBperDOLLAR}
TEAMS = ['总', '010', '075', '060', '080']

Q_START = datetime.datetime(2020, 10, 1)

TABLE_COLS = ['Team', '  季度目标', '  日均目标', '已完成利润', '平均日利润', '平均利润差', '剩余季度目标', '剩余日目标',
              ' 平均日收入', ' 平均日消耗', ' 昨日组收入', ' 昨日组消耗']


def quarter_target_table(data, rmb=False):
    d_table = pd.DataFrame(columns=TABLE_COLS)
    data['profit'] = data['earnings'] - data['spend']
    data = data[data['date'] >= Q_START]

    dates = data.date.unique()
    date_str = str(dates[0])[:10] + ' ~ ' + str(dates[-1])[:10]
    day_range = len(dates)

    if rmb:
        div_factor = 1
    else:
        div_factor = RMBperDOLLAR

    for team in TEAMS:
        apps = TEAM_APPS.get(team)
        data_team = data[data['app'].isin(apps)]

        day_revenue = data_team.earnings.sum()/day_range  # 平均日收入
        day_cost = data_team.spend.sum()/day_range        # 平均日消耗

        day_target = TEAM_TAR.get(team)              # 日均目标
        q_done = data_team.profit.sum()              # 已完成利润
        q_target = 92 * day_target                   # 季度目标
        day_done = q_done/day_range                  # 平均日利润
        day_diff = (day_target*day_range - q_done)/day_range  # 平均利润差
        q_todo = q_target - q_done                   # 剩余季度目标
        day_todo = q_todo/(92 - day_range)           # 剩余日目标

        last_day_data = data_team[data_team['date'] >= dates[-1]]
        last_day_revenue = last_day_data.earnings.sum()
        last_day_cost = last_day_data.spend.sum()

        values = [team]
        values.extend([int(v/div_factor) for v in [q_target, day_target, q_done, day_done, day_diff, q_todo, day_todo,
                                                   day_revenue, day_cost, last_day_revenue, last_day_cost]])
        new1 = pd.DataFrame([values], columns=TABLE_COLS)
        d_table = d_table.append(new1)

    return d_table, date_str


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
    selector_id = app + '_date_range'
    return dcc.RadioItems(id=selector_id,
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
    sumxy = data.earnings - data.spend
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=data.earnings, name='Profit'))
    fig.add_trace(go.Bar(x=x, y=-data.spend, name='Cost'))
    fig.add_trace(go.Scatter(x=x, y=sumxy, mode='lines+markers', name='Gross'))
    gross_profit = int(sum(data.earnings) - sum(data.spend))
    fig.update_layout(barmode='relative',
                      title_text=name+'      = '+str(gross_profit))
    return fig


def get_apps_checklist(selector_id):
    options = [{'label': app, 'value': app} for app in APPS]
    return dcc.Checklist(id=selector_id, options=options, value=APPS)


def data_loader(cost_path='cost.csv', revenue_path='revenue.csv'):
    cost = pd.read_csv(cost_path)
    cost['date'] = cost['date'].apply(pd.to_datetime)

    revenue = pd.read_csv(revenue_path)
    revenue['date'] = revenue['date'].apply(pd.to_datetime)

    data = pd.merge(cost, revenue, on=['date', 'app'])
    data = data[['date', 'app', 'spend', 'earnings']]
    data = data.sort_values(by=['date'])
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(data)
    return data

