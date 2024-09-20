import streamlit as st
from eliza import create_eliza

# Set the page title and layout
st.set_page_config(page_title="Eliza Chatbot", layout="centered", initial_sidebar_state="auto")

# Apply custom dark mode theme settings with layout fixes
st.markdown(
    """
    <style>
    body {
        background-color: #343541;
        color: white;
    }
    .stTextInput, .stButton {
        background-color: #40414f;
        color: white;
    }
    div[role="textbox"] > * {
        background-color: #40414f !important;
        color: white !important;
    }
    .stApp {
        background-color: #343541;
        color: white;
    }
    /* Customize title color and size */
    .css-18ni7ap h1, .css-10trblm {
        color: white !important;
        font-size: 3em !important;
        font-weight: bold !important;
        text-align: center;
    }
    /* Customize input box */
    .stTextInput input {
        border-radius: 10px !important;
        padding: 10px !important;
        background-color: #40414f !important;
        border: 2px solid #00BFFF !important; /* Deep sky blue border */
        color: white !important;  /* Make input text white */
    }
    /* Chat message bubbles */
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 70%;
        color: white !important; /* Make chat messages white */
    }
    .user-message {
        background-color: #00BFFF;
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .eliza-message {
        background-color: #40414f;
        color: white;
        align-self: flex-start;
    }
    /* Layout for buttons side by side */
    .button-container {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        gap: 10px; /* Add space between buttons */
    }
    .stButton > button {
        background-color: #00BFFF !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 1.1em !important;
        width: 100%; /* Full width for each button in flex */
    }
    /* Hover effect for the buttons */
    .stButton > button:hover {
        background-color: #1E90FF !important;
        color: white !important;
    }
    /* Footer styling */
    footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #343541;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the Eliza chatbot
if 'eliza' not in st.session_state:
    st.session_state.eliza = create_eliza()
    st.session_state.conversation = []  # Store the conversation history

# Function to handle sending user input
def send_message():
    user_input = st.session_state.user_input.strip()
    
    if user_input:
        # Append the user input to the conversation history
        st.session_state.conversation.append(f"You: {user_input}")
        
        # Get the response from Eliza
        eliza_response = st.session_state.eliza.respond(user_input)
        
        # Append Eliza's response to the conversation history
        if eliza_response:
            st.session_state.conversation.append(f"Eliza: {eliza_response}")
        else:
            st.session_state.conversation.append(st.session_state.eliza.final())
        
        # Clear input after sending
        st.session_state.user_input = ""

# Title of the app
st.markdown('<p style="font-family:Courier; color:white; font-size: 40px; text-align: center;">Eliza Chatbot</p>', unsafe_allow_html=True)

# Display the conversation history
for message in st.session_state.conversation:
    if message.startswith("You:"):
        st.markdown(f"<div class='chat-bubble user-message'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble eliza-message'>{message}</div>", unsafe_allow_html=True)



# Input text box for user input with a callback for sending messages on enter and hiding label
user_input = st.text_input("Chat input", label_visibility="collapsed", key="user_input", on_change=send_message)

# Add a "Send" button and "Reset Conversation" button side by side
st.markdown('<div class="button-container">', unsafe_allow_html=True)
send_button = st.button("Send")
reset_button = st.button("Reset Conversation")
st.markdown('</div>', unsafe_allow_html=True)

if send_button:
    send_message()

if reset_button:
    st.session_state.conversation = []
    st.session_state.eliza = create_eliza()

# Footer with name and website link
st.markdown(
    """
    <footer>
        Created by <a href="https://sainesh.com" target="_blank" style="color: #00BFFF; text-decoration: none;">Sainesh Nakra</a>
    </footer>
    """,
    unsafe_allow_html=True
)
