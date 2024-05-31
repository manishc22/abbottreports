from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_master_data import kyc_master
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

st.set_page_config(page_title="KYC Details",
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

st.write('#### KYC Details')
df_details = kyc_master()
st.write('##### Region wise KYC Audits')
st.write('   ')
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "**:blue[KYC Master Status]**", df_details.shape[0])

with col2:
    st.metric(
        "**:blue[KYC Success]**", df_details[df_details['KYC Status'] ==
                                             'Success'].shape[0])

with col3:
    st.metric(
        "**:blue[KYC Failed]**", df_details[df_details['KYC Status'] ==
                                            'Failed'].shape[0])
st.write('  ')
st.dataframe(df_details,  hide_index=True,
             use_container_width=True)
