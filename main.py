import streamlit as st
import openai
import re


# Set page configuration
st.set_page_config(page_title="Script Writing Assistant", layout="centered")

# OpenAI API Key (Replace with a secure method)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# Function to clean and format response
def clean_and_format_response(response_text):
    response_text = re.sub(r"\*\*(.*?)\*\*", r"\1", response_text)  # Remove bold markdown
    response_text = re.sub(r"\*(.*?)\*", r"\1", response_text)  # Remove italics
    response_text = re.sub(r"###\s*(.*)", r"**\1**", response_text)  # Convert ### headings to bold
    response_text = re.sub(r"##\s*(.*)", r"**\1**", response_text)  # Convert ## headings to bold
    response_text = re.sub(r"#\s*(.*)", r"**\1**", response_text)  # Convert # headings to bold
    response_text = response_text.replace("_", "")  # Remove stray underscores
    response_text = response_text.strip()  # Trim spaces
    return response_text

# Function to generate script using OpenAI
def generate_script(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": "You are a professional screenplay writer. Format your response properly with well-structured text and charcter introduction. If the user asks anything else, politely refuse to answer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.5
    )
    raw_text = response["choices"][0]["message"]["content"]
    return clean_and_format_response(raw_text)

# --- UI DESIGN ---

# Logo & Title (Keeps it at the top)
with st.container():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("logo.png", use_container_width=True)
    with col2:
        st.markdown('<div class="header-title">Script Writing Assistant 📜</div>', unsafe_allow_html=True)
st.markdown("---")

# Output Section (Script display area)
if "script_text" in st.session_state and st.session_state.script_text:
    st.subheader("🎬 Generated Script")
    st.write(st.session_state.script_text)  

# Spacer to push input box to the bottom
st.markdown("<div style='height: 30vh;'></div>", unsafe_allow_html=True)

# User Input (Placed at the bottom)
st.subheader("Enter Your Script Prompt Below:")
user_prompt = st.text_area("Describe your script scene...", key="script_prompt")

if st.button("Generate Script"):
    if user_prompt.strip():
        with st.spinner("Writing your script..."):
            script_text = generate_script(user_prompt)  # Get formatted response
            st.session_state.script_text = script_text  # Store in session
            st.rerun()  # Refresh page to display output above
    else:
        st.warning("⚠️ Please enter a valid prompt.")

# Footer
st.markdown("<br><br><center>🔹 **Copyright @ immerso.ai 2025**</center>", unsafe_allow_html=True)
