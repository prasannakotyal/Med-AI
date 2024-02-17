import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="MediChat",
    page_icon=":brain:",
    layout="wide",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []

def medichat_app():
    st.title("👩‍⚕️- MediChat (Your personal medical assistant)")

    # Display the chat history
    for message in st.session_state.chat_session:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask medichat...")
    if user_prompt:
        # Add user's message to chat and display it
        st.session_state.chat_session.append({"role": "user", "parts": [{"text": user_prompt}]})
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = model.start_chat(history=[user_prompt])

        # Display Gemini-Pro's response
        st.session_state.chat_session.append({"role": "model", "parts": [{"text": gemini_response.parts[0].text}]})
        with st.chat_message("assistant"):
            st.markdown(gemini_response.parts[0].text)
