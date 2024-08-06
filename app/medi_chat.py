import streamlit as st
from dotenv import load_dotenv
import ollama

# Load environment variables
load_dotenv()

def medichat_app():
    # Initialize session state for messages and full message
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you with your health today?"}]

    if "full_message" not in st.session_state:
        st.session_state["full_message"] = ""

    # Display the message history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖").write(msg["content"])

    # Function to generate a response
    def generate_response():
        response = ollama.chat(model='llama2', stream=True, messages=st.session_state.messages)
        for partial_resp in response:
            token = partial_resp["message"]["content"]
            st.session_state["full_message"] += token
            yield token

    # User input handling
    prompt = st.chat_input("Type your message here...")

    if prompt:
        # Add user input to message history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="🧑‍💻").write(prompt)
        
        # Add instruction to the system message for appropriate responses
        professional_instruction = (
            "You are a medical assistant providing basic medical information. Offer accurate, helpful, and polite responses based on established medical knowledge. "
            "While you should be informative, ensure to advise users to consult a healthcare professional for personalized medical advice or serious concerns. "
            "Provide clear explanations about symptoms, treatments, and general health tips as appropriate."
        )
        st.session_state.messages.append({"role": "system", "content": professional_instruction})

        # Generate the assistant's response
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
