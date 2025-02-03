import streamlit as st

st.set_page_config(page_title="API Key Debugger")

if "OPENAI_API_KEY" in st.secrets:
    st.write("✅ API key is set correctly!")
else:
    st.error("❌ API key is missing in Streamlit secrets. Please check settings.")
