# diet_recommender.py

import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

def diet_recommender_app():
    st.title("🍏 Diet Recommender")

    # Initialize st.session_state if not already initialized
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # User input form
    age = st.slider("Age", 1, 100, 25)
    gender = st.radio("Gender", ["Male", "Female"])
    weight = st.slider("Weight (KG)", 40.0, 200.0, 70.0)
    height = st.slider("Height (CM)", 100.0, 250.0, 170.0)
    
    # Merged option for diet preference
    diet_preference = st.radio("Diet Preference", ["Veg", "Non-Veg"])
    
    disease = st.text_input("Generic Disease (if any)", "")
    region = st.text_input("Region (e.g., Asia, North America)", "")
    allergics = st.text_input("Allergies (if any)", "")

    # New option for workout preference
    workout_preference = st.radio("Workout Preference", ["Cardio", "Strength Training", "Yoga", "Any"])

    # Submit button
    if st.button("Get Recommendations"):
        # Prepare user input for the Google API
        user_input = (
            f"Age: {age}\n"
            f"Gender: {gender.lower()}\n"
            f"Weight: {weight}\n"
            f"Height: {height}\n"
            f"Diet Preference: {diet_preference.lower()}\n"
            f"Generic Disease: {disease}\n"
            f"Region: {region}\n"
            f"Allergies: {allergics}\n"
            f"Workout Preference: {workout_preference}"
        )

        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_input)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_input)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
