import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Function to handle the MediChat app
def medichat_app():
    # Display the chatbot's title on the page
    st.title("‍⚕️ MediChat - Your Medical Assistant")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask MediChat...")
    if user_prompt:
        # Add user's message to chat and display it
        st.session_state.chat_session.add_user_message(user_prompt)
        st.chat_message("user").markdown(user_prompt)

# Streamlit UI
st.title("Welcome to Care Compass")

# Create tabs
tabs = ["MediChat", "Calorie Tracker", "Nearby Places"] # Add "Diet Recommender"
selected_tab = st.radio("Choose Option", tabs)

# Display the selected tab
if selected_tab == "MediChat":
    medichat_app()
elif selected_tab == "Calorie Tracker":
    calorie_tracker_app()
elif selected_tab == "Nearby Places":
    nearby_places_app()
# elif selected_tab == "Diet Recommender":  # Add this block for the Diet Recommender tab
#     diet_recommender_app()
