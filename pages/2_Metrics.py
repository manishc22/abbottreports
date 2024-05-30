from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import master_view, total_count

import numpy as np
import altair as alt
import plotly.graph_objects as go


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Project Metrics",
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
if df_filter.shape[0] > 0:
    count = total_count().values[0]
    col10, col11, col12, col13, col14 = st.columns(5, gap='small')
    with col10:
        st.write("### *Overview*")
    # print(df_filter[df_filter['RMName'] == ''])
    # Total Forms Filled
    with col11:
        st.metric(
            "**:blue[Total Audits]**", df_filter.shape[0])
# Incorrect Position IDs
    with col12:
        st.metric("**:blue[Incorrect Position IDs]**",
                  df_filter[df_filter['RMName'] == 'None'].shape[0])
# Stores not in Master DB
    with col13:
        st.metric("**:blue[Stores not in Master DB]**",
                  df_filter[df_filter['store_name_updated'] == 'None'].shape[0])

# Selfie with Dealerboard (%)
    with col11:
        selfie = round(df_filter[df_filter['selfie_dealerboard']
                                 == True].shape[0] * 100 / df_filter.shape[0], 1)
        st.metric("**:blue[Selfie with Dealerboard (%)]**",
                  selfie)
# Bad Image Quality (%)
        image_quality = round(df_filter[df_filter['image_quality']
                                        == False].shape[0] * 100 / df_filter.shape[0], 1)
    with col12:
        st.metric("**:blue[Bad Image Quality (%)]**",
                  image_quality)

    with col13:
        st.metric("**TOTAL FORMS FILLED**",
                  count)

    st.divider()
    col10, col11, col12, col13, col14 = st.columns(5, gap='small')

    with col10:
        st.write("### *Pediasure*")

# Window Visibility Pediasure (%)
    window_viz_ps = round(df_filter[df_filter['p_window_exist']
                                    == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col11:
        st.metric("**:blue[Window Visibility (%)]**",
                  window_viz_ps)

# Pediasure 4 shelf strip
    ps_shelf = round(df_filter[df_filter['p_four_shelf_strip']
                               == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col12:
        st.metric("**:blue[4 Shelf Strip (%)]**",
                  ps_shelf)
# Pediasure Eye Level
    ps_eye_level = round(df_filter[df_filter['p_eye_level']
                                   == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col13:
        st.metric("**:blue[Eye Level (%)]**",
                  ps_eye_level)

    ps_backing = round(df_filter[df_filter['p_backing_sheet']
                                 == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col14:
        st.metric("**:blue[Backing Sheet (%)]**",
                  ps_backing)

    st.divider()
    col10, col11, col12, col13, col14 = st.columns(5, gap='small')

    with col10:
        st.write("### *Ensure*")

    window_viz_es = round(df_filter[df_filter['e_window_exist']
                                    == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col11:
        st.metric("**:blue[Window Visibility (%)]**",
                  window_viz_es)

# Pediasure 4 shelf strip
    es_shelf = round(df_filter[df_filter['e_four_shelf_strip']
                               == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col12:
        st.metric("**:blue[4 Shelf Strip (%)]**",
                  es_shelf)
# Pediasure Eye Level
    es_eye_level = round(df_filter[df_filter['e_eye_level']
                                   == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col13:
        st.metric("**:blue[Eye Level (%)]**",
                  es_eye_level)

    es_backing = round(df_filter[df_filter['e_backing_sheet']
                                 == True].shape[0] * 100 / df_filter.shape[0], 1)
    with col14:
        st.metric("**:blue[Backing Sheet (%)]**",
                  es_backing)
else:
    st.write("#### No Data Available")
    # Window Visibility Ensure (%)
    # Ensure 4 shelf strip
    # Ensure Eye Level
    # All must-win Brands (%)
