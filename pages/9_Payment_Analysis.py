import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title="Payment Analysis",
                   layout='wide', initial_sidebar_state='expanded')

# st.markdown(
#     """
# <style>
#     [data-testid="collapsedControl"] {
#         display: none
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )
df_raw = pd.read_excel("Sales.xlsx", sheet_name="Sheet1")
df_zero = df_raw[df_raw["Total Payout (Rs)"] == 0]

st.write('#### Overview')
col1, col2, col3 = st.columns([1, 1, 4], gap='large')
with col1:
    st.metric('Total Stores', df_raw.shape[0])
with col2:
    st.metric('Stores with zero payments', df_zero.shape[0])
total = round(df_raw['Total Payout (Rs)'].sum(), 1)
with col3:
    st.metric('Total Payments', total.sum())
st.divider()
with st.expander(label='### Payment Analysis'):
    components.iframe('https://embed.deepnote.com/8fb5748f-8fc7-4d4a-9fec-9ea603ee251a/14e830f941614c8491f92448466b0629/985acb2d122c4ccf9ce08f7535d94abf?height=507', height=600,
                      width=None, scrolling=False)

with st.expander(label='Target Vs Achievement'):
    components.iframe('https://embed.deepnote.com/8fb5748f-8fc7-4d4a-9fec-9ea603ee251a/14e830f941614c8491f92448466b0629/9ab9e10f18c84114af8af4336d4ea564?height=507', height=600,
                      width=None, scrolling=False)
