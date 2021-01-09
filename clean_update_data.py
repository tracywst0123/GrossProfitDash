import pandas as pd
from gross_profit_dash_app.data_config import BUNDLE_LIST


def clean_earnings(df=None, path='/Users/tracy/Desktop/revenue_new.csv'):
    if not df:
        df = pd.read_csv(path)
    df['earnings'] = df['Impression'] * df['ECPM']/1000
    df = df.rename(columns={'App': 'app', 'Date': 'date'})
    df = df[['app', 'date', 'earnings']]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    df.to_csv(path)
    df = pd.read_csv(path)
    return df


def clean_cost_pay(df, path='/Users/tracy/Desktop/cost_pay_new.csv'):
    df.to_csv(path)
    df = pd.read_csv(path)
    invert_app = {j: i for (i, j) in BUNDLE_LIST}
    df = df.rename(columns={'bundle_id': 'app'})
    df['app'] = df['app'].map(invert_app)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    df = df[df.app.notnull()]
    return df


def concact_data(path, df_new, cols):
    print(df_new)
    original = pd.read_csv(path)
    print(original)
    combined = pd.concat([original, df_new])
    combined = combined[cols]
    combined = combined[combined.app.notnull()]
    print(combined)
    combined.to_csv(path)


if __name__ == '__main__':
    cost_pay_new_path = '/Users/tracy/Desktop/cost_pay_new.csv'
    cleaned_cost_pay = clean_cost_pay(pd.read_csv(cost_pay_new_path))

    concact_data('data/cost.csv',
                 cleaned_cost_pay[['app', 'date', 'spend']],
                 cols=['date', 'app', 'spend'])

    concact_data('data/pay.csv',
                 cleaned_cost_pay[['app', 'date', 'pay']],
                 cols=['date', 'app', 'pay'])

    revenue_new_path = '/Users/tracy/Desktop/revenue_new.csv'
    revenue_new = clean_earnings(path=revenue_new_path)

    concact_data('data/revenue.csv', revenue_new, cols=['date', 'app', 'earnings'])


