from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import master_view, audit_data, overview_data, daily_forms, weekly_data, total_audits

import numpy as np
import altair as alt
import plotly.graph_objects as go


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Audit Reports",
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
                'SUB-D'] = str(int(df_overview['SUB-D'].sum()))
df_overview.loc['Total',
                'None'] = str(int(df_overview['None'].sum()))

df_audit_data.loc['Total',
                  'Pediasure Window Visibility'] = str(int(df_audit_data['Pediasure Window Visibility'].sum()))
df_audit_data.loc['Total',
                  'Ensure Window Visibility'] = str(int(df_audit_data['Ensure Window Visibility'].sum()))
df_audit_data.loc['Total',
                  'All Brands Exist'] = str(int(df_audit_data['All Brands Exist'].sum()))

# df_master = df_master['RMName'].replace('', np.nan, regex=True)

col1, col2, col3, col4, col5, col6 = st.columns(
    [0.5, 0.5, 1, 0.75, 0.5, 1])
with col1:
    month = st.selectbox(
        "Select Month", df_master['month'].drop_duplicates(), key=0.1)

    st.divider()

col1, col2 = st.columns([8, 1], gap='large')
with col1:
    col20, col21, col22 = st.columns([4, 1, 1], gap='large')
    with col20:
        df_overview_f = df_overview[(df_overview['Month'] == month)]
        df_overview_f.loc['Total', 'RegionName'] = 'Total'
        df_overview_f.loc['Total',
                          'Forms Received'] = int(df_overview_f['Forms Received'].sum())
        df_overview_f.loc['Total',
                          'Images Audited'] = int(df_overview_f['Images Audited'].sum())
        df_overview_f.loc['Total',
                          'Samrat'] = int(df_overview_f['Samrat'].sum())
        df_overview_f.loc['Total',
                          'SUB-D'] = int(df_overview_f['SUB-D'].sum())
        df_overview_f.loc['Total',
                          'Hygeine Corner'] = int(df_overview_f['Hygeine Corner'].sum())
        df_overview_f.loc['Total',
                          'None'] = int(df_overview_f['None'].sum())
        df_audit_f = df_audit_data[(df_audit_data['Month'] == month)]

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
            "Month": None, "Cycle": None, "Yuvraj": None})

    with col21:
        df_total = total_audits()

        st.metric(
            "**:blue[Total Stores]**", df_total['count'])
    with col22:
        pct_coverage = round(df_overview_f.loc['Total',
                                               'Forms Received']*100/df_total['count'], 2)
        st.metric(
            "**:blue[% Coverage]**", pct_coverage)

    st.divider()
with col1:
    st.write("##### Audit Summary")

    st.dataframe(df_audit_f,  hide_index=True, column_config={
        "Month": None, "Cycle": None}, use_container_width=True)
    st.divider()

with col1:

    chart = alt.Chart(df_daily[df_daily['month'] == month], title='Daily Forms Filled').mark_bar().encode(
        x=alt.X('created_at', sort=None, title='Date'),
        y=alt.Y('total',
                title='Total Forms'),
    )
    st.altair_chart(chart,  use_container_width=True)
    # st.line_chart(df_daily, x='created_at', y='total')

    df_weekly_forms = weekly_data(month)
    weeks = df_weekly_forms['Week Start / End'].drop_duplicates().values

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
