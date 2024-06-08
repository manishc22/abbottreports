import io
import pandas as pd
import streamlit as st
from functions.get_master_data import kyc_total_data, kyc_regional_data, kyc_master_data, kyc_daily_forms
import time
import altair as alt
import xlsxwriter


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

# total_count = kyc_total_data()
df_regional = kyc_regional_data()


df_regional.rename(
    columns={"program_name": "ProgramName", "count": "Total KYCs"}, inplace=True)
df_master = kyc_master_data()
df_master.rename(columns={"customer_count": "Total Stores"}, inplace=True)
col1, col2, col3 = st.columns([1, 5, 1], gap='large')
df_regional.set_index(['RegionName', 'ProgramName'], inplace=True)
df_master.set_index(['RegionName', 'ProgramName'], inplace=True)

# Concatenate along the columns
df_final = pd.concat([df_regional, df_master], axis=1).reset_index()

df_final['% Coverage'] = round(
    df_final['Total KYCs'] * 100 / df_final['Total Stores'], 1)
total_count = df_final['Total KYCs'].sum()
df_final.loc['Total', 'Total KYCs'] = df_final['Total KYCs'].sum()
df_final.loc['Total', 'Total Stores'] = df_final['Total Stores'].sum()
df_final.loc['Total', '% Coverage'] = round(
    df_final['Total KYCs'].sum() * 100 / df_final['Total Stores'].sum(), 1)
df_final.loc['Total', 'ProgramName'] = 'Total'

with col1:
    st.metric(
        "**:blue[Total KYCs]**", total_count)

with col2:
    st.write('##### Region wise KYC Audits')
    col11, col12 = st.columns([3, 1])
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
