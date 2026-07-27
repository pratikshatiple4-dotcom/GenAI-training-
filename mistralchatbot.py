import os
import streamlit as st
from mistralai.client import Mistral
st.title("Free Mistral API Chatbot")

MISTRAL_API_KEY = None
if "MISTRAL" in st.secrets:
    MISTRAL_API_KEY = st.secrets["MISTRAL"].get("api_key")

if not MISTRAL_API_KEY:
    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    st.error(
        "❗ Add your Mistral API key in .streamlit/secrets.toml under [MISTRAL] api_key, "
        "or set the environment variable MISTRAL_API_KEY."
    )
    st.stop()

client = Mistral(api_key="EEnucsx8aNAdD4klbqUbe07QEdJnbhQ8")
if "history" not in st.session_state:
    st.session_state["history"] = []
user_input = st.text_input("Enter your message:")

def get_mistral_response(user_message):
    # build the chat messages list
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    # Call the Mistral LLM chat complete endpoint
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
    )

    if not getattr(response, "choices", None):
        return ""

    first_choice = response.choices[0]
    message = getattr(first_choice, "message", None)
    if not message or getattr(message, "content", None) is None:
        return ""

    content = message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(getattr(chunk, "content", "") for chunk in content)
    return str(content)

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        # Get reply from Mistral
        reply = get_mistral_response(user_input)
        st.session_state.history.append({"role": "assistant", "content": reply})

for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**AI:** {chat['content']}")