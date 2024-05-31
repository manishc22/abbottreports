from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import tse_exception, zero_isr
from datetime import date
import time
import numpy as np
import altair as alt
import plotly.graph_objects as go


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="KYC Exceptions",
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

st.write('### KYC Exceptions')
st.write('   ')
df_tse = tse_exception()
st.write('##### TSE Exceptions')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "**:blue[> 20% KYCs remaining]**", df_tse.shape[0])

with col1:
    st.metric(
        "**:blue[Total Stores Remaining (North)]**", df_tse[df_tse['RegionName'] == 'North']['Remaining Stores'].sum())

with col2:
    st.metric(
        "**:blue[Total Stores Remaining (East)]**", df_tse[df_tse['RegionName'] == 'EAST']['Remaining Stores'].sum())

with col3:
    st.metric(
        "**:blue[Total Stores Remaining (West)]**", df_tse[df_tse['RegionName'] == 'WEST']['Remaining Stores'].sum())

with col2:
    st.metric(
        "**:blue[Total Stores Remaining (South 1)]**", df_tse[df_tse['RegionName'] == 'SOUTH 1']['Remaining Stores'].sum())

with col3:
    st.metric(
        "**:blue[Total Stores Remaining (South 2)]**", df_tse[df_tse['RegionName'] == 'South 2']['Remaining Stores'].sum())

st.dataframe(df_tse,  hide_index=True,
             use_container_width=True)

st.write('   ')

st.write('##### Zero ISRs')
df_isr = zero_isr()
col10, col11, col12 = st.columns(3)
with col10:
    st.metric(
        "**:blue[Total Zero ISRs]**", df_isr['ISRPositionID'].count())

with col11:
    st.metric(
        "**:blue[Zero ISRs (North)]**", df_isr[df_isr['RegionName'] == 'North']['ISRPositionID'].count())

with col12:
    st.metric(
        "**:blue[Zero ISRs (East)]**", df_isr[df_isr['RegionName'] == 'EAST']['ISRPositionID'].count())

st.dataframe(df_isr,  hide_index=True,
             use_container_width=True)
