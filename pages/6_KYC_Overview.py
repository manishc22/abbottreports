import io
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import kyc_total_data, kyc_regional_data, kyc_master_data, kyc_daily_forms
from datetime import date
import time
import numpy as np
import altair as alt
import plotly.graph_objects as go
from st_aggrid import AgGrid
import xlsxwriter

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="KYC Overview",
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
t = time.localtime()
current_time = time.strftime("%H:%M", t)
# st.write(f'##### As on: {date.today()}, {current_time} ')
st.write('#### KYC Metrics')
st.write('    ')
total_count = kyc_total_data()
df_regional = kyc_regional_data()
df_regional.rename(
    columns={"program_name": "ProgramName", "count": "Total KYCs"}, inplace=True)
df_master = kyc_master_data()
df_master.rename(columns={"count": "Total Stores"}, inplace=True)
col1, col2, col3 = st.columns([1, 5, 1], gap='large')
df_regional.set_index(['RegionName', 'ProgramName'], inplace=True)
df_master.set_index(['RegionName', 'ProgramName'], inplace=True)

# Concatenate along the columns
df_final = pd.concat([df_regional, df_master], axis=1).reset_index()

df_final['% Coverage'] = round(
    df_final['Total KYCs'] * 100 / df_final['Total Stores'], 1)

df_final.loc['Total', 'Total KYCs'] = df_final['Total KYCs'].sum()
df_final.loc['Total', 'Total Stores'] = df_final['Total Stores'].sum()
df_final.loc['Total', '% Coverage'] = round(
    df_final['Total KYCs'].sum() * 100 / df_final['Total Stores'].sum(), 1)
df_final.loc['Total', 'ProgramName'] = 'Total'
# print(df_final)
with col1:
    st.metric(
        "**:blue[Total KYCs]**", total_count['count'][0])

# gb = GridOptionsBuilder.from_dataframe(df_final)

# gb.configure_default_column(
#     groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
# gb.configure_pagination(paginationAutoPageSize=True)
# gb.configure_grid_options(domLayout='normal')
# gb.configure_side_bar()
# gridOptions = gb.build()

with col2:
    st.write('##### Region wise KYC Audits')
    col11, col12 = st.columns([5, 1], gap='large')
    with col12:
        def to_excel(df) -> bytes:
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine="xlsxwriter")
            df.to_excel(writer, sheet_name="Sheet1")
            writer.close()
            processed_data = output.getvalue()
            return processed_data

        st.download_button(
            "Download as excel",
            data=to_excel(df_final),
            file_name="output.xlsx",
            mime="application/vnd.ms-excel",
        )

    st.dataframe(df_final, hide_index=True, use_container_width=True)
    st.write('   ')
    df_daily = kyc_daily_forms()
    chart = alt.Chart(df_daily, title='Daily KYCs').mark_bar().encode(
        x=alt.X('created_at', sort=None, title='Date'),
        y=alt.Y('total',
                title='Total KYCs'),
    )
    st.altair_chart(chart,  use_container_width=True)
