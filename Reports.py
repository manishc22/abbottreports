from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import master_view, total_count
import numpy as np


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Audit Reports",
                   layout='wide', initial_sidebar_state='expanded')


df_master = master_view()
df_master.replace("", "None", inplace=True)
print(df_master['RMName'])
# df_master = df_master['RMName'].replace('', np.nan, regex=True)

tab1, tab2, tab3 = st.tabs(["Dashboard", "Dealerboard", "Window Visibility"])
with tab1:

    rm_list = np.append(
        ["Cumulative"], df_master['RMName'].drop_duplicates().to_numpy())

    program_list = np.append(
        ["All"], df_master['program_name'].drop_duplicates().to_numpy())

    col1, col2, col3, col4, col5, col6 = st.columns(
        [0.5, 0.5, 1, 0.75, 0.5, 1])
    with col1:
        month = st.selectbox(
            "Select Month", df_master['month'].drop_duplicates())
    with col2:
        cycle = st.selectbox(
            "Select Cycle", df_master['cycle'].drop_duplicates())
    with col3:
        rm = st.selectbox(
            "Select RM", rm_list)
    with col4:
        program = st.selectbox(
            "Program Name", program_list)

    with col6:
        view = st.selectbox(
            "Select View", ['Key Metrics', 'Data Tables'])
    st.divider()

    if (rm == 'Cumulative') and (program == 'All'):
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle)]
    if rm != 'Cumulative' and program == 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['RMName'] == rm)]
    if rm == 'Cumulative' and program != 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['program_name'] == program)]
    if rm != 'Cumulative' and program != 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['program_name'] == program) & (df_master['RMName'] == rm)]
    count = total_count().values[0]

    if view == 'Key Metrics':
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
    # Window Visibility Ensure (%)
    # Ensure 4 shelf strip
    # Ensure Eye Level
    # All must-win Brands (%)

    if view == 'Data Tables':
        st.data_editor(df_filter, hide_index=True, column_config={
            "id": None,
            "image1_id": None,
            "image2_id": None,
            "RMName": None,
            "program_name": None,
            "store_name_updated": None,
            "month": None,
            "cycle": None,
            "created_at": "Date",
            "position_id": "Sales Position ID",
            "store_name": "Store Name",
            "SalesmanName": "Salesman"

        },
        )
with tab2:
    if 'counter' not in st.session_state:
        st.session_state['counter'] = 0

    counter = st.session_state.counter

    rm_list = np.append(
        ["Cumulative"], df_master['RMName'].drop_duplicates().to_numpy())

    program_list = np.append(
        ["All"], df_master['program_name'].drop_duplicates().to_numpy())

    salesman = np.append(
        ["All"], df_master['SalesmanName'].drop_duplicates().to_numpy())

    asm = np.append(
        ["All"], df_master['ASMName'].drop_duplicates().to_numpy())

    col1, col2, col3, col4, col5, col6 = st.columns(
        [0.5, 0.5, 1, 1, 1, 1])
    with col1:
        month = st.selectbox(
            "Select Month", df_master['month'].drop_duplicates(), key=2.1)
    with col2:
        cycle = st.selectbox(
            "Select Cycle", df_master['cycle'].drop_duplicates(), key=2.2)
    with col3:
        rm = st.selectbox(
            "Select RM", rm_list, key=2.3)
    with col4:
        program = st.selectbox(
            "Program Name", program_list, key=2.4)

    # with col5:
    #     asm = st.selectbox(
    #         "Select ASM", asm, key=2.5)
    st.divider()

    if (rm == 'Cumulative') and (program == 'All'):
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle)]
    if rm != 'Cumulative' and program == 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['RMName'] == rm)]
    if rm == 'Cumulative' and program != 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['program_name'] == program)]
    if rm != 'Cumulative' and program != 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['program_name'] == program) & (df_master['RMName'] == rm)]
    count = total_count().values[0]

    col1, col2 = st.columns([1, 5], gap='large')
    with col1:
        st.checkbox("Selfie with Dealerboard")
        df_new = df_filter[df_filter['selfie_dealerboard'] == True]

with tab3:
    st.header("Window Visibility Reporting")
