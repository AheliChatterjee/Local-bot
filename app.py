import streamlit as st
import ollama

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- SESSION STATES ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processing" not in st.session_state:
    st.session_state.processing = False

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ Settings")

    selected_model = st.selectbox(
        "Choose Model",
        ["phi3", "tinyllama"]
    )

    system_prompt = st.text_area(
        "System Prompt",
        value="""
You are a professional AI assistant.

Rules:
1. Answer clearly and directly.
2. Keep answers concise.
3. Do not invent meanings of names.
4. Remember conversation context accurately.
5. Be friendly and professional.
"""
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- MAIN UI ----------------

st.title("🤖 Local AI Chatbot")
st.caption("Powered by Ollama + Streamlit")

# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------

prompt = None

if not st.session_state.processing:
    prompt = st.chat_input("Ask something...")

# ---------------- HANDLE USER MESSAGE ----------------

if prompt:

    # lock input
    st.session_state.processing = True

    # store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # rerun immediately to hide input
    st.rerun()

# ---------------- GENERATE RESPONSE ----------------

# only run if:
# last message is from user
# AND currently processing

if (
    st.session_state.processing
    and len(st.session_state.messages) > 0
    and st.session_state.messages[-1]["role"] == "user"
):

    
    

    # assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = ollama.chat(
                model=selected_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ] + st.session_state.messages[-6:]
            )

            bot_reply = response["message"]["content"]

            st.markdown(bot_reply)

    # save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    # unlock input
    st.session_state.processing = False

    # rerun to show input again
    st.rerun()