from openai import OpenAI
import streamlit as st

client = OpenAI()

my_assistant = client.beta.assistants.create(
    instructions="You are a professional scriptwriter. Write long and detailed scripts. If the user asks anything else, politely refuse to answer.",
    name="Script Writing Assistant",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

def generate_script(prompt):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=my_assistant.id
    )
    
    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages.data[0].content[0].text.value
    else:
        return "An error occurred while generating the script."

# Streamlit UI
st.set_page_config(page_title="Script Writing Assistant", layout="wide")
st.image("logo.png", width=150)
st.title("📜 Script Writing Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
chat_container = st.container()
for message in st.session_state.chat_history:
    with chat_container:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")

# User input
st.markdown("---")
user_input = st.text_area("Enter your script prompt:", key="user_prompt", label_visibility="collapsed")

if st.button("Generate Script"):
    if user_input.strip():
        with st.spinner("Generating your script..."):
            script_response = generate_script(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": script_response})
            st.markdown(f"**Assistant:** {script_response}")
    else:
        st.warning("Please enter a valid prompt.")

st.write("_Powered by Immerso AI_ 🚀")
