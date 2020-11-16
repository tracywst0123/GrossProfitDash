import numpy as np
import pandas as pd
import datetime


def convert_excel_time(excel_time):
    return pd.to_datetime('1899-12-30') + pd.to_timedelta(excel_time, 'D')