import pandas as pd
from gross_profit_dash_app.dash_utils import APP_LIST


def clean_earnings(df):
    cols = ['app', 'date', 'earnings']
    df['earnings'] = df['Impression'] * df['ECPM']/1000
    df = df.rename(columns={'App': 'app', 'Date': 'date'})
    df = df[cols]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    return df


def clean_cost(df):
    invert_app = {j: i for (i, j) in APP_LIST}
    df = df.rename(columns={'bundle_id': 'app'})
    df['app'] = df['app'].map(invert_app)
    df = df[['app', 'date', 'spend']]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    return df


def clean_pay(df):
    invert_app = {j: i for (i, j) in APP_LIST}
    df = df.rename(columns={'bundle_id': 'app'})
    df['app'] = df['app'].map(invert_app)
    df = df[['app', 'date', 'pay']]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    return df


# def data_loader(cost_path='cost.csv', revenue_path='revenue.csv'):
#     cost = clean_cost(pd.read_csv(cost_path))
#     revenue = clean_earnings(pd.read_csv(revenue_path))
#     data = pd.merge(cost, revenue, on=['date', 'app'])
#     data = data[['date', 'app', 'spend', 'earnings']]
#     data = data.sort_values(by=['date'])
#     return data

if __name__ == '__main__':
    cost_new_path = '/Users/tracy/Desktop/cost_new.csv'
    cost_new = pd.read_csv(cost_new_path)
    cost_new = cost_new.sort_values(by=['date'])
    cost_new.to_csv(cost_new_path)
    cost_new = clean_cost(pd.read_csv(cost_new_path))
    print(cost_new)

    cost_path = 'data/cost.csv'
    cost = pd.read_csv(cost_path)
    print(cost)
    cost = pd.concat([cost, cost_new])
    cost = cost[['date', 'app', 'spend']]
    cost = cost[cost.app.notnull()]
    print(cost)
    cost.to_csv(cost_path)

    pay_new_path = '/Users/tracy/Desktop/pay_new.csv'
    pay_new = pd.read_csv(pay_new_path)
    pay_new = pay_new.sort_values(by=['date'])
    pay_new.to_csv(pay_new_path)
    pay_new = clean_pay(pd.read_csv(pay_new_path))
    print(pay_new)

    pay_path = 'data/pay.csv'
    pay = pd.read_csv(pay_path)
    print(pay)
    pay = pd.concat([pay, pay_new])
    pay = pay[['date', 'app', 'pay']]
    pay = pay[pay.app.notnull()]
    print(pay)
    pay.to_csv(pay_path)

    revenue_new_path = '/Users/tracy/Desktop/revenue_new.csv'
    revenue_new = pd.read_csv(revenue_new_path)
    revenue_new = clean_earnings(revenue_new)
    revenue_new.to_csv(revenue_new_path)
    revenue_new = pd.read_csv(revenue_new_path)
    print(revenue_new)

    revenue_path = 'data/revenue.csv'
    revenue = pd.read_csv(revenue_path)
    print(revenue)
    revenue = pd.concat([revenue, revenue_new])
    revenue = revenue[['date', 'app', 'earnings']]
    print(revenue)
    revenue.to_csv(revenue_path)

