import streamlit as st
from medi_chat import medichat_app
from calorie_tracker import calorie_tracker_app
from nearby_places import nearby_places_app
# from diet_recommender import diet_recommender_app  # Import the diet_recommender app

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
