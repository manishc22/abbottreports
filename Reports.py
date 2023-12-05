from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import master_view, total_count, audit_data, overview_data, daily_forms
import numpy as np
import altair as alt

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Audit Reports",
                   layout='wide', initial_sidebar_state='expanded')


df_master = master_view()
df_master.replace("", "None", inplace=True)
df_audit_data = audit_data()
df_audit_data.replace("", "None", inplace=True)

df_overview = overview_data()
df_overview.replace("", "None", inplace=True)

df_daily = daily_forms()
df_overview.loc['Total',
                'Forms Received'] = str(int(df_overview['Forms Received'].sum()))
df_overview.loc['Total',
                'Images Audited'] = str(int(df_overview['Images Audited'].sum()))
df_overview.loc['Total',
                'Samrat'] = str(int(df_overview['Samrat'].sum()))
df_overview.loc['Total',
                'Yuvraj'] = str(int(df_overview['Yuvraj'].sum()))
df_overview.loc['Total',
                'None'] = str(int(df_overview['None'].sum()))

df_audit_data.loc['Total',
                  'Pediasure Window Visibility'] = str(int(df_audit_data['Pediasure Window Visibility'].sum()))
df_audit_data.loc['Total',
                  'Ensure Window Visibility'] = str(int(df_audit_data['Ensure Window Visibility'].sum()))
df_audit_data.loc['Total',
                  'All Brands Exist'] = str(int(df_audit_data['All Brands Exist'].sum()))

# df_master = df_master['RMName'].replace('', np.nan, regex=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Drilldowns", "Dealerboard", "Window Visibility"])
with tab1:

    col1, col2, col3, col4, col5, col6 = st.columns(
        [0.5, 0.5, 1, 0.75, 0.5, 1])
    with col1:
        month = st.selectbox(
            "Select Month", df_master['month'].drop_duplicates(), key=0.1)
    with col2:
        cycle = st.selectbox(
            "Select Cycle", df_master['cycle'].drop_duplicates(), key=0.2)
    st.divider()

    col1, col2 = st.columns([1, 2], gap='large')
    with col1:

        df_overview_f = df_overview[(df_overview['Month'] == month) & (
            df_overview['Cycle'] == cycle)]
        df_overview_f.loc['Total',
                          'Forms Received'] = int(df_overview_f['Forms Received'].sum())
        df_overview_f.loc['Total',
                          'Images Audited'] = int(df_overview_f['Images Audited'].sum())
        df_overview_f.loc['Total',
                          'Samrat'] = int(df_overview_f['Samrat'].sum())
        df_overview_f.loc['Total',
                          'Yuvraj'] = int(df_overview_f['Yuvraj'].sum())
        df_overview_f.loc['Total',
                          'None'] = int(df_overview_f['None'].sum())
        df_audit_f = df_audit_data[(df_audit_data['Month'] == month) & (
            df_audit_data['Cycle'] == cycle)]

        df_audit_f.loc['Total',
                       'Audited'] = int(df_audit_f['Audited'].sum())
        df_audit_f.loc['Total',
                       'Pediasure Window Visibility'] = int(df_audit_f['Pediasure Window Visibility'].sum())
        df_audit_f.loc['Total',
                       'Ensure Window Visibility'] = int(df_audit_f['Ensure Window Visibility'].sum())
        df_audit_f.loc['Total',
                       'All Brands Exist'] = int(df_audit_f['All Brands Exist'].sum())
        df_audit_f.loc['Total',
                       'Good Image Quality'] = int(df_audit_f['Good Image Quality'].sum())
        df_audit_f.loc['Total',
                       'Selfie with Dealerboard'] = int(df_audit_f['Selfie with Dealerboard'].sum())
        df_audit_f.loc['Total',
                       'Stores not in DB'] = int(df_audit_f['Stores not in DB'].sum())
        st.write("##### Overview")
        st.dataframe(df_overview_f, hide_index=True, column_config={
                     "Month": None, "Cycle": None})
        st.divider()
    with col2:
        st.write("##### Audit Summary")

        st.dataframe(df_audit_f,  hide_index=True, column_config={
            "Month": None, "Cycle": None})
        st.divider()
    with col1:

        chart = alt.Chart(df_daily, title='Daily Forms Filled').mark_bar().encode(
            x=alt.X('created_at', sort=None, title='Date'),
            y=alt.Y('total',
                    title='Total Forms'),
        )
        st.altair_chart(chart,  use_container_width=True)
        # st.line_chart(df_daily, x='created_at', y='total')
with tab2:

    region_list = np.append(
        ["Cumulative"], df_master['RegionName'].drop_duplicates().to_numpy())

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
        region_list = st.selectbox(
            "Select Region", region_list)
    with col4:
        program = st.selectbox(
            "Program Name", program_list)

    with col6:
        view = st.selectbox(
            "Select View", ['Key Metrics', 'Data Tables'])
    st.divider()

    if (region_list == 'Cumulative') and (program == 'All'):
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle)]
    if region_list != 'Cumulative' and program == 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['RegionName'] == region_list)]
    if region_list == 'Cumulative' and program != 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['program_name'] == program)]
    if region_list != 'Cumulative' and program != 'All':
        df_filter = df_master[(df_master['month'] == month)
                              & (df_master['cycle'] == cycle) & (df_master['program_name'] == program) & (df_master['RegionName'] == region_list)]
    if df_filter.shape[0] > 0:
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
    else:
        st.write("#### No Data Available")
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
with tab3:
    if 'counter' not in st.session_state:
        st.session_state['counter'] = 0

    counter = st.session_state.counter

    def reset_counter():
        print("RESET")
        st.session_state.counter = 0

    region_list = np.append(
        ["Cumulative"], df_master['RegionName'].drop_duplicates().to_numpy())

    program_list = np.append(
        ["All"], df_master['program_name'].drop_duplicates().to_numpy())

    col1, col2, col3, col4, col5, col6 = st.columns(
        [0.5, 0.5, 1, 1, 1, 1])
    with col1:
        month = st.selectbox(
            "Select Month", df_master['month'].drop_duplicates(), key=2.1)
    with col2:
        cycle = st.selectbox(
            "Select Cycle", df_master['cycle'].drop_duplicates(), key=2.2)
    with col3:
        region = st.selectbox(
            "Select Region", region_list, key=2.3)
    with col4:
        program = st.selectbox(
            "Program Name", program_list, key=2.4)

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

    col1, col2, col3 = st.columns([1, 0.25, 4], gap='large')
    with col1:
        st.caption("Filters")
        selfie = st.checkbox("Selfie with Dealerboard")
        st.divider()
        df_new = df_filter[df_filter['selfie_dealerboard']
                           == selfie].reset_index(drop=True)

        salesman_list = np.append(
            ["All"], df_new['SalesmanName'].drop_duplicates().to_numpy())

        asm_list = np.append(
            ["All"], df_new['ASMName'].drop_duplicates().to_numpy())

        asm = st.selectbox(
            "Select ASM", asm_list, key=2.5)

        if asm == "All":
            df_final = df_new
        else:
            df_final = df_new[df_new['ASMName'] == asm].reset_index(drop=True)
        # salesman = st.selectbox(
        #     "Select Salesman", salesman_list, key=2.6)

    with col3:
        print("Counter+ " + str(counter))
        if df_final.shape[0] > 0:
            total_images = df_final.shape[0]

            col11, col12, col13, col14, col15 = st.columns(
                [1, 3, 1, 1, 1], gap='small')
            with col11:
                st.write(
                    f"##### Image Number: {st.session_state.counter + 1} of {total_images}")

                df_final.loc[counter, 'created_at'] = pd.to_datetime(
                    df_final.loc[counter, 'created_at']) + pd.Timedelta('05:30:00')

            id = df_final.loc[counter, 'id']
            position_id = df_final.loc[counter, 'position_id']
            image = df_final.loc[counter, 'image1_id']

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
                print(counter)
                st.session_state.counter += 1

            def decrement_counter():
                st.session_state.counter -= 1
            with col14:
                st.button("Previous Page", on_click=decrement_counter)
            with col15:
                st.button("Next Page", on_click=increment_counter)
            st.divider()
            st.image(image_url)
        else:
            st.write("No data available")

with tab4:
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
        # salesman = st.selectbox(
        #     "Select Salesman", salesman_list, key=2.6)

    with col3:

        if df_final.shape[0] > 0:
            total_images = df_final.shape[0]

            col11, col12, col13, col14, col15 = st.columns(
                [1, 3, 1, 1, 1], gap='small')
            with col11:
                st.write(
                    f"##### Image Number: {st.session_state.win_counter + 1} of {total_images}")

                df_final.loc[counter, 'created_at'] = pd.to_datetime(
                    df_final.loc[counter, 'created_at']) + pd.Timedelta('05:30:00')

            id = df_final.loc[counter, 'id']
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
