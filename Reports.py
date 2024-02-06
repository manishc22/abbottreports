from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import master_view, total_count, audit_data, overview_data, daily_forms, sales_team, sales_count, sales_team_total, sales_store_master, total_sales_visits, weekly_data

import numpy as np
import altair as alt
import plotly.graph_objects as go



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
df_daily['date'] = pd.to_datetime(df_daily['created_at'])
df_daily['month'] = df_daily['date'].dt.strftime('%b')

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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Sales Team Adoption", "Drilldowns", "Dealerboard", "Window Visibility"])
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

        chart = alt.Chart(df_daily[df_daily['month']==month], title='Daily Forms Filled').mark_bar().encode(
            x=alt.X('created_at', sort=None, title='Date'),
            y=alt.Y('total',
                    title='Total Forms'),
        )
        st.altair_chart(chart,  use_container_width=True)
        # st.line_chart(df_daily, x='created_at', y='total')

    df_weekly_forms = weekly_data(month)
    weeks = df_weekly_forms['Week Start / End'].drop_duplicates().values
    print(weeks)
    # with col2:
    
        
    fig1 = go.Figure(data=[
        go.Bar(name='Forms Filled (North)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'NORTH']['Weekly Forms Filled']),
        go.Bar(name='Weekly Targets (North)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'NORTH']['Weekly Target']),    
        go.Bar(name='Forms Filled (East)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'EAST']['Weekly Forms Filled']),
        go.Bar(name='Weekly Targets (East)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'EAST']['Weekly Target']),     
        go.Bar(name='Forms Filled (West)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'WEST']['Weekly Forms Filled']),
        go.Bar(name='Weekly Targets (West)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'WEST']['Weekly Target']),         
        go.Bar(name='Forms Filled (South1)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'SOUTH 1']['Weekly Forms Filled']),
        go.Bar(name='Weekly Targets (South1)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'SOUTH 1']['Weekly Target']),         
        go.Bar(name='Forms Filled (South2)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'SOUTH 2']['Weekly Forms Filled']),
        go.Bar(name='Weekly Targets (South2)',
            x=weeks, y=df_weekly_forms[df_weekly_forms['RegionName'] == 'SOUTH 2']['Weekly Target']),             

        
    ])
    fig1.update_layout(barmode='group', title=f"Weekly Region-wise Form Submissions ({month})", xaxis_title="Weeks",
                    yaxis_title="Total Count",
                    legend_title="Bar Type",)
    
    st.plotly_chart(fig1, use_container_width=True)

    


with tab2:
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
            "Select Month", df_sales_team['month'].drop_duplicates())    

    with col3:
        cycle = st.selectbox(
            "Select Cycle", df_sales_team['cycle'].drop_duplicates())    
    if (region != 'Cumulative'):
        df_filter = df_sales_team[(df_sales_team['RegionName'] == region) & (df_sales_team['month'] == month) & (df_sales_team['cycle'] == cycle)]
        df_asm_count = df_sales_team['FLMPositionId'][(df_sales_team['month'] == month) & (df_sales_team['cycle'] == cycle) & (df_sales_team['RegionName'] == region)].drop_duplicates().shape[0]
        df_asm_total = df_sales_count[(df_sales_count['RegionName'] == region)]['total_asm'].sum()
        df_sales_total = df_sales_count[(df_sales_count['RegionName'] == region)]['total_salesmen'].sum()
        df_sales_team_total_filtered = df_sales_team_total[df_sales_team_total['RegionName'] == region]
    else:
        df_filter = df_sales_team[(df_sales_team['month'] == month) & (df_sales_team['cycle'] == cycle)]
        df_asm_count = df_sales_team[(df_sales_team['month'] == month) & (df_sales_team['cycle'] == cycle)]['FLMPositionId'].drop_duplicates().shape[0]
        df_asm_total = df_sales_count['total_asm'].sum()
        df_sales_total = df_sales_count['total_salesmen'].sum()
        df_sales_team_total_filtered = df_sales_team_total

    st.divider()
    df_subtract = df_sales_team_total_filtered[df_sales_team_total_filtered.SalesmanPositionID.isin(df_filter.position_id) == False]
    df_filter_stores_1 = df_total_sales_visits[(df_total_sales_visits['month'] == month) & (df_total_sales_visits['cycle'] == cycle)]
    df_filter.reset_index(inplace = True)
    i = 0
    
    while i < df_filter.shape[0]:
        df_filter.loc[i,'unique_visits'] = df_filter_stores_1[df_filter_stores_1['position_id'] == df_filter.loc[i,'position_id']].shape[0]
        df_filter.loc[i,'coverage'] = round(df_filter.loc[i,'unique_visits']*100 / df_filter.loc[i,'total_stores'], 1)
        df_filter.loc[i, 'repeats'] = round(df_filter.loc[i,'total_forms']*100 / df_filter.loc[i,'unique_visits'], 1)
        i = i + 1
        

    st.write('##### Salesmen with at least 1 form filled during this cycle')
    col5, col6, col7, col8 = st.columns([1, 1, 1, 2])

    with col5:
        
        st.metric(
            "**:blue[Total Salesmen]**", f"{df_filter.shape[0]} / {df_sales_total}")
    
    with col6:
        st.metric(
            "**:blue[Total ASM]**", f"{df_asm_count} / {df_asm_total}")

    with col7:
        st.metric(
            "**:blue[Average Coverage %]**", round(df_filter['coverage'].mean(), 1))    
    st.data_editor(df_filter, hide_index=True, column_config={'month':None, 'cycle': None, 'index': None, 'coverage': 'Coverage %', 'repeats': 'Repeats %', 'total_forms':'Total Forms', 'total_stores': 'Total Stores in Master', 'unique_visits': '# Unique Store Visits'})
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
        st.data_editor(df_subtract, hide_index=True, column_config={'RegionName':None})

    
    with col6:
        
        ASM = st.selectbox(
            "Select ASM", df_filter['FLMPositionId'].drop_duplicates())    
        position_id = st.selectbox(
            "Select Salesman", df_filter[df_filter['FLMPositionId'] == ASM]['position_id'].drop_duplicates())   

    with col7:

        st.write('####  ')
        salesman = df_filter[(df_filter['position_id'] == position_id)]['SalesmanName'].drop_duplicates().values[0]
        st.write(f'##### Salesman: {salesman}')    
        df_master_stores = sales_store_master()
        df_filter_master = df_master_stores[df_master_stores['SalesmanPositionID'] == position_id]
        df_filter_stores = df_total_sales_visits[(df_total_sales_visits['month'] == month) & (df_total_sales_visits['cycle'] == cycle) & (df_total_sales_visits['position_id'] == position_id)]
        df_store_subtract = df_filter_master[df_filter_master.StoreName.isin(df_filter_stores.store_name_updated) == False]
        
        st.data_editor(df_filter_stores, hide_index=True, column_config={'month':None, 'cycle':None, 'position_id': None})
        st.divider()
        st.write('##### Stores with zero visits')
        col1, col2 = st.columns(2)
        with col1:
            metric = df_filter[df_filter['position_id'] == position_id]['total_stores'].values[0]
        
            st.metric(
                "**:blue[Total Stores with zero visits]**", f'{df_store_subtract.shape[0]} / {metric}')
        with col2:    
            st.data_editor(df_store_subtract, hide_index=True, column_config={'SalesmanPositionID': None})

with tab3:

    region_list = np.append(
        ["Cumulative"], df_master['RegionName'].drop_duplicates().to_numpy())

    program_list = np.append(
        ["All"], df_master['program_name'].drop_duplicates().to_numpy())

    col1, col2, col3, col4, col5, col6 = st.columns(
        [0.5, 0.5, 1, 0.75, 0.5, 1])
    with col1:
        month = st.selectbox(
            "Select Month", df_master['month'].drop_duplicates(), key='tab3_month')
    with col2:
        cycle = st.selectbox(
            "Select Cycle", df_master['cycle'].drop_duplicates(), key = 'tab3_cycle')
    with col3:
        region_list = st.selectbox(
            "Select Region", region_list)
    with col4:
        program = st.selectbox(
            "Program Name", program_list)

    with col6:
        view = st.selectbox(
            "Select View", ['Data Tables', 'Key Metrics'])
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


with tab4:
    if 'counter' not in st.session_state:
        st.session_state['counter'] = 0

    counter = st.session_state.counter

    def reset_counter():
        
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

with tab5:
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
