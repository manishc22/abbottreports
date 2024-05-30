from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import master_view

import numpy as np
import altair as alt
import plotly.graph_objects as go


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Detailed Datatables",
                   layout='wide', initial_sidebar_state='expanded')
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
df_master = master_view()
df_master.replace("", "None", inplace=True)

region_list = np.append(
    ["Cumulative"], df_master['RegionName'].drop_duplicates().to_numpy())

program_list = np.append(
    ["All"], df_master['program_name'].drop_duplicates().to_numpy())

col1, col2, col3, col4, col5, col6 = st.columns(
    [0.5, 0.5, 1, 0.75, 0.5, 1])
with col1:
    month = st.selectbox(
        "Select Month", df_master['month'].drop_duplicates(), key='tab3_month')

with col3:
    region_list = st.selectbox(
        "Select Region", region_list)
with col4:
    program = st.selectbox(
        "Program Name", program_list)


st.divider()

if (region_list == 'Cumulative') and (program == 'All'):
    df_filter = df_master[(df_master['month'] == month)]
if region_list != 'Cumulative' and program == 'All':
    df_filter = df_master[(df_master['month'] == month)
                          & (df_master['RegionName'] == region_list)]
if region_list == 'Cumulative' and program != 'All':
    df_filter = df_master[(df_master['month'] == month)
                          & (df_master['program_name'] == program)]
if region_list != 'Cumulative' and program != 'All':
    df_filter = df_master[(df_master['month'] == month)
                          & (df_master['program_name'] == program) & (df_master['RegionName'] == region_list)]

st.data_editor(df_filter, hide_index=True, column_config={
    "id": None,
    "image1_id": None,
    "image2_id": None,
    "RMName": None,
    "program_name": None,
    "store_name_updated": None,
    "month": None,
    "cycle": None,
    "ASMName": None,
    "created_at": "Date",
    "position_id": "Sales Position ID",
    "store_name": "Store Name",
    "SalesmanName": "Salesman"

},
)
