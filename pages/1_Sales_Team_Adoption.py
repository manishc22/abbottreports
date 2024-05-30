from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import sales_team, sales_count, sales_team_total, sales_store_master, total_sales_visits

import numpy as np
import altair as alt
import plotly.graph_objects as go


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Sales Team Adoption",
                   layout='wide', initial_sidebar_state='collapsed')

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
df_sales_team = sales_team()
df_sales_count = sales_count()
df_sales_team_total = sales_team_total()
df_total_sales_visits = total_sales_visits()
regions = np.append(
    ["Cumulative"], df_sales_team['RegionName'].drop_duplicates().to_numpy())
col1, col2, col3, col4 = st.columns(
    [0.5, 0.5, 0.5, 0.75])

with col1:
    region = st.selectbox(
        "Select Region", regions)

with col2:
    month = st.selectbox(
        "Select Month", df_sales_team['month'].drop_duplicates().sort_values(ascending=False))

if (region != 'Cumulative'):
    df_filter = df_sales_team[(df_sales_team['RegionName'] == region) & (
        df_sales_team['month'] == month)]
    df_asm_count = df_sales_team['FLMPositionId'][(df_sales_team['month'] == month) & (
        df_sales_team['RegionName'] == region)].drop_duplicates().shape[0]
    df_asm_total = df_sales_count[(
        df_sales_count['RegionName'] == region)]['total_asm'].sum()
    df_sales_total = df_sales_count[(
        df_sales_count['RegionName'] == region)]['total_salesmen'].sum()
    df_sales_team_total_filtered = df_sales_team_total[df_sales_team_total['RegionName'] == region]
else:
    df_filter = df_sales_team[(df_sales_team['month'] == month)]
    df_asm_count = df_sales_team[(
        df_sales_team['month'] == month)]['FLMPositionId'].drop_duplicates().shape[0]
    df_asm_total = df_sales_count['total_asm'].sum()
    df_sales_total = df_sales_count['total_salesmen'].sum()
    df_sales_team_total_filtered = df_sales_team_total

st.divider()
df_subtract = df_sales_team_total_filtered[df_sales_team_total_filtered.SalesmanPositionID.isin(
    df_filter.position_id) == False]
df_filter_stores_1 = df_total_sales_visits[(
    df_total_sales_visits['month'] == month)]
df_filter.reset_index(inplace=True)
i = 0

while i < df_filter.shape[0]:
    df_filter.loc[i, 'unique_visits'] = df_filter_stores_1[df_filter_stores_1['position_id']
                                                           == df_filter.loc[i, 'position_id']].shape[0]
    df_filter.loc[i, 'coverage'] = round(
        df_filter.loc[i, 'unique_visits']*100 / df_filter.loc[i, 'total_stores'], 1)
    df_filter.loc[i, 'repeats'] = round(
        df_filter.loc[i, 'total_forms']*100 / df_filter.loc[i, 'unique_visits'], 1)
    i = i + 1

st.write('##### Salesmen with at least 1 form filled during this cycle')
col5, col6, col7, col8 = st.columns([1, 1, 1, 2])
print(df_filter)
with col5:

    st.metric(
        "**:blue[Total Salesmen]**", f"{df_filter.shape[0]} / {df_sales_total}")

with col6:
    st.metric(
        "**:blue[Total ASM]**", f"{df_asm_count} / {df_asm_total}")

with col7:
    st.metric(
        "**:blue[Average Coverage %]**", round(df_filter['coverage'].mean(), 1))
st.data_editor(df_filter, hide_index=True, column_config={'month': None, 'cycle': None, 'index': None, 'coverage': 'Coverage %',
               'repeats': 'Repeats %', 'total_forms': 'Total Forms', 'total_stores': 'Total Stores in Master', 'unique_visits': '# Unique Store Visits'})
st.divider()
col10, col11 = st.columns(2)
with col10:
    st.write(f'##### Region: {region}')
with col11:
    st.write('#### Store Coverage')

col5, col6, col7 = st.columns([2, 1, 4], gap='large')
with col5:

    st.metric(
        "**:blue[Total Salesmen with 0 forms]**", df_subtract.shape[0])
    st.data_editor(df_subtract, hide_index=True,
                   column_config={'RegionName': None})

with col6:

    ASM = st.selectbox(
        "Select ASM", df_filter['FLMPositionId'].drop_duplicates())
    position_id = st.selectbox(
        "Select Salesman", df_filter[df_filter['FLMPositionId'] == ASM]['position_id'].drop_duplicates())

with col7:

    st.write('####  ')
    salesman = df_filter[(df_filter['position_id'] == position_id)
                         ]['SalesmanName'].drop_duplicates().values[0]
    st.write(f'##### Salesman: {salesman}')
    df_master_stores = sales_store_master()
    df_filter_master = df_master_stores[df_master_stores['SalesmanPositionID'] == position_id]
    df_filter_stores = df_total_sales_visits[(df_total_sales_visits['month'] == month) & (
        df_total_sales_visits['position_id'] == position_id)]
    df_store_subtract = df_filter_master[df_filter_master.StoreName.isin(
        df_filter_stores.store_name_updated) == False]

    st.data_editor(df_filter_stores, hide_index=True, column_config={
                   'month': None, 'cycle': None, 'position_id': None})
    st.divider()
    st.write('##### Stores with zero visits')
    col1, col2 = st.columns(2)
    with col1:
        metric = df_filter[df_filter['position_id']
                           == position_id]['total_stores'].values[0]

        st.metric(
            "**:blue[Total Stores with zero visits]**", f'{df_store_subtract.shape[0]} / {metric}')
    with col2:
        st.data_editor(df_store_subtract, hide_index=True,
                       column_config={'SalesmanPositionID': None})
