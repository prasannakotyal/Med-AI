import streamlit as st
import google.generativeai as gen_ai

def medichat_app():
    # Set up Google Gemini-Pro AI model
    gen_ai.configure(api_key="YOUR_GOOGLE_API_KEY")  # Replace "YOUR_GOOGLE_API_KEY" with your actual API key
    model = gen_ai.GenerativeModel('gemini-pro')

    # Function to translate roles between Gemini-Pro and Streamlit terminology
    def translate_role_for_streamlit(user_role):
        if user_role == "model":
            return "assistant"
        else:
            return user_role

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Streamlit UI
    st.title("Welcome to MediChat")

    # Display MediChat tab
    st.title("👩‍⚕️- MediChat (Your personal medical assistant)")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.text_input("Ask MediChat...")
    if user_prompt:
        # Add user's message to chat and display it
        st.session_state.chat_session.history.append(user_prompt)  # Append user's message to history

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
