import streamlit.components.v1 as components
import streamlit as st

st.set_page_config(page_title="Payment Analysis",
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
with st.expander(label='Overview'):
    components.iframe('https://embed.deepnote.com/8fb5748f-8fc7-4d4a-9fec-9ea603ee251a/14e830f941614c8491f92448466b0629/f07cae534207473eb20cfc887d170970?height=441', height=600,
                      width=None, scrolling=False)

with st.expander(label='Payment to Stores'):
    components.iframe('https://embed.deepnote.com/8fb5748f-8fc7-4d4a-9fec-9ea603ee251a/14e830f941614c8491f92448466b0629/985acb2d122c4ccf9ce08f7535d94abf?height=507', height=600,
                      width=None, scrolling=False)

with st.expander(label='Distribution of Target Vs Achievement'):
    components.iframe('https://embed.deepnote.com/8fb5748f-8fc7-4d4a-9fec-9ea603ee251a/14e830f941614c8491f92448466b0629/9ab9e10f18c84114af8af4336d4ea564?height=507', height=600,
                      width=None, scrolling=False)
