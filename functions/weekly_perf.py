import pandas as pd
from .get_master_data import weekly_data

import xlsxwriter

from datetime import date

def weekly_report(month):
    today = date.today()
    df_weeks = weekly_data(month)
    var = list(df_weeks['RegionName'].drop_duplicates().values)
    weeks = list(df_weeks['Week Start / End'].drop_duplicates().values)
    
    ind = pd.MultiIndex.from_product([var])
    cols = pd.MultiIndex.from_product([weeks, ['Total Target', 'Weekly Target', 'Weekly Forms Filled', 'Target Achieved %']])
    df_new = pd.DataFrame(df_weeks, index = ind, columns = cols)
    i = 0
    while i < df_weeks.shape[0]:
        df_new.loc[df_weeks.loc[i,'RegionName'], (df_weeks.loc[i,'Week Start / End'], 'Total Target')] = df_weeks.loc[i, 'Total Target']
        df_new.loc[df_weeks.loc[i,'RegionName'], (df_weeks.loc[i,'Week Start / End'], 'Weekly Target')] = df_weeks.loc[i, 'Weekly Target']
        df_new.loc[df_weeks.loc[i,'RegionName'], (df_weeks.loc[i,'Week Start / End'], 'Weekly Forms Filled')] = df_weeks.loc[i, 'Weekly Forms Filled']
        df_new.loc[df_weeks.loc[i,'RegionName'], (df_weeks.loc[i,'Week Start / End'], 'Target Achieved %')] = df_weeks.loc[i, 'Target Achieved %']
        i = i + 1
    

    for week in weeks:
        df_new.loc['Total', (week, 'Total Target')] = df_new[(week, 'Total Target')].sum()
        df_new.loc['Total', (week, 'Weekly Target')] = df_new[(week, 'Weekly Target')].sum()
        df_new.loc['Total', (week, 'Weekly Forms Filled')] = df_new[(week, 'Weekly Forms Filled')].sum()
        df_new.loc['Total', (week, 'Target Achieved %')] = df_new[(week, 'Target Achieved %')].mean()

    return df_new
    