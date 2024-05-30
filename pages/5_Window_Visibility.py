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

st.set_page_config(page_title="Window Visibility",
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

if 'win_counter' not in st.session_state:
    st.session_state['win_counter'] = 0

counter = st.session_state.win_counter

# def reset_counter():
#     print("RESET")
#     st.session_state.counter = 0

region_list = np.append(
    ["Cumulative"], df_master['RegionName'].drop_duplicates().to_numpy())

program_list = np.append(
    ["All"], df_master['program_name'].drop_duplicates().to_numpy())

col1, col2, col3, col4, col5, col6 = st.columns(
    [0.5, 0.5, 1, 1, 1, 1])
with col1:
    month = st.selectbox(
        "Select Month", df_master['month'].drop_duplicates(), key=3.1)
with col2:
    cycle = st.selectbox(
        "Select Cycle", df_master['cycle'].drop_duplicates(), key=3.2)
with col3:
    region = st.selectbox(
        "Select Region", region_list, key=3.3)
with col4:
    program = st.selectbox(
        "Program Name", program_list, key=3.4)

st.divider()

if (region == 'Cumulative') and (program == 'All'):
    df_filter = df_master[(df_master['month'] == month)
                          & (df_master['cycle'] == cycle)]
if region != 'Cumulative' and program == 'All':
    df_filter = df_master[(df_master['month'] == month)
                          & (df_master['cycle'] == cycle) & (df_master['RegionName'] == region)]
if region == 'Cumulative' and program != 'All':
    df_filter = df_master[(df_master['month'] == month)
                          & (df_master['cycle'] == cycle) & (df_master['program_name'] == program)]
if region != 'Cumulative' and program != 'All':
    df_filter = df_master[(df_master['month'] == month)
                          & (df_master['cycle'] == cycle) & (df_master['program_name'] == program) & (df_master['RegionName'] == region)]
# print(df_master)
col1, col2, col3 = st.columns([1, 0.25, 4], gap='large')
with col1:

    # image_quality = st.checkbox("Image Quality")
    # all_brands = st.checkbox("All Brands Available")
    # st.caption("Pediasure")
    # p_window_exist = st.checkbox("Window Exist", key=1)
    # p_eye_level = st.checkbox("Eye Level", key=2)
    # p_backing_sheet = st.checkbox("Backing Sheet", key=3)
    # p_four_shelf = st.checkbox("4 Shelf Strip", key=4)

    # st.caption("Ensure")
    # e_window_exist = st.checkbox("Window Exist", key=5)
    # e_eye_level = st.checkbox("Eye Level", key=6)
    # e_backing_sheet = st.checkbox("Backing Sheet", key=7)
    # e_four_shelf = st.checkbox("4 Shelf Strip", key=8)

    # st.divider()
    # df_new = df_filter[(df_filter['image_quality']
    #                    == image_quality) & (df_filter['all_brands']
    #                    == all_brands)].reset_index(drop=True)

    salesman_list = np.append(
        ["All"], df_filter['SalesmanName'].drop_duplicates().to_numpy())

    asm_list = np.append(
        ["All"], df_filter['ASMName'].drop_duplicates().to_numpy())

    asm = st.selectbox(
        "Select ASM", asm_list, key=3.5)

    if asm == "All":
        df_final = df_filter.reset_index(drop=True)
    else:
        df_final = df_filter[df_filter['ASMName']
                             == asm].reset_index(drop=True)
    st.divider()
    total_p_window = df_final[df_final['p_window_exist']
                              == True]['p_window_exist'].sum()
    total_e_window = df_final[df_final['e_window_exist']
                              == True]['e_window_exist'].sum()
    total_p_brand = df_final[df_final['p_backing_sheet']
                             == True]['p_backing_sheet'].sum()
    total_e_brand = df_final[df_final['e_backing_sheet']
                             == True]['e_backing_sheet'].sum()

    st.write(
        f"###### Total Window Exists (Pediasure): {total_p_window}")
    st.write(
        f"###### Total Window Exists (Ensure): {total_e_window}")
    st.write(
        f"###### Total Brand Block (Pediasure): {total_p_brand}")
    st.write(
        f"###### Total Brand Block (Ensure): {total_e_brand}")

    # salesman = st.selectbox(
    #     "Select Salesman", salesman_list, key=2.6)

with col3:

    if df_final.shape[0] > 0:
        total_images = df_final.shape[0]

        col11, col12, col13, col14, col15 = st.columns(
            [1, 3, 1, 1, 1], gap='small')
        with col11:
            id = df_final.loc[counter, 'id']
            st.write(f"##### ID: {id}")
            st.write(
                f"##### Image Number: {st.session_state.win_counter + 1} of {total_images}")

            df_final.loc[counter, 'created_at'] = pd.to_datetime(
                df_final.loc[counter, 'created_at']) + pd.Timedelta('05:30:00')

        position_id = df_final.loc[counter, 'position_id']
        image = df_final.loc[counter, 'image2_id']

        date = df_final.loc[counter, 'created_at'].strftime('%d')
        month = df_final.loc[counter, 'created_at'].strftime('%b')
        time = df_final.loc[counter, 'created_at'].strftime('%X')
        store_updated = df_final.loc[counter, 'store_name_updated']
        store = df_final.loc[counter, 'store_name']
        if store_updated:
            store_final = store_updated
        else:
            store_final = store

        image_url = storage_url + image

        msg = "Date: " + date + " " + month + " " + \
            time + " |  " + cycle + " |  " + store
        with col12:
            st.write(f"##### PositionID - {position_id}")
            st.write(f"###### {msg}")

        def increment_counter():
            st.session_state.win_counter += 1

        def decrement_counter():
            st.session_state.win_counter -= 1
        with col14:
            st.button("Previous Page", on_click=decrement_counter, key=100)
        with col15:
            st.button("Next Page", on_click=increment_counter, key=101)
        st.divider()
        st.image(image_url)
    else:
        st.write("No data available")
