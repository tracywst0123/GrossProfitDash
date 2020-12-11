import pandas as pd
from gross_profit_dash_app.dash_utils import data_loader, quarter_target_table


def convert_excel_time(excel_time):
    return pd.to_datetime('1899-12-30') + pd.to_timedelta(excel_time, 'D')


if __name__ == '__main__':
    data = data_loader()
    table, d_str = quarter_target_table(data)

    table.to_excel('/Users/tracy/Downloads/profit_table.xlsx')