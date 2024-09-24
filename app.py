import streamlit as st
from eliza import create_eliza

# Set the page title and layout
st.set_page_config(page_title="Eliza Chatbot", layout="centered", initial_sidebar_state="auto")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Eliza Chatbot", "About Eliza", "Chat History"])

# Apply the custom CSS for dark mode
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
    .css-18ni7ap h1, .css-10trblm {
        color: white !important;
        font-size: 3em !important;
        font-weight: bold !important;
        text-align: center;
    }
    .stTextInput input {
        border-radius: 10px !important;
        padding: 10px !important;
        background-color: #40414f !important;
        border: 2px solid #00BFFF !important; 
        color: white !important;
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 70%;
        color: white !important;
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
    .button-container {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        gap: 10px;
    }
    .stButton > button {
        background-color: #00BFFF !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 1.1em !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1E90FF !important;
        color: white !important;
    }
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

# Page-specific logic
if page == "Eliza Chatbot":
    # Initialize the Eliza chatbot
    if 'eliza' not in st.session_state:
        st.session_state.eliza = create_eliza()
        st.session_state.conversation = []

    # Function to handle sending user input
    def send_message():
        user_input = st.session_state.user_input.strip()
        
        if user_input:
            st.session_state.conversation.append(f"You: {user_input}")
            eliza_response = st.session_state.eliza.respond(user_input)
            
            if eliza_response:
                st.session_state.conversation.append(f"Eliza: {eliza_response}")
            else:
                st.session_state.conversation.append(st.session_state.eliza.final())
            
            st.session_state.user_input = ""
    
    # Define the reset_conversation function to handle the reset logic
    def reset_conversation():
        st.session_state.conversation = []
        st.session_state.eliza = create_eliza()
        st.session_state.user_input = ""

    # Title of the app
    st.markdown('<p style="font-family:Courier; color:white; font-size: 40px; text-align: center;">Eliza Chatbot </p>', unsafe_allow_html=True)

    # Display the conversation history
    for message in st.session_state.conversation:
        if message.startswith("You:"):
            st.markdown(f"<div class='chat-bubble user-message'>{message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble eliza-message'>{message}</div>", unsafe_allow_html=True)

    # Input text box for user input
    st.text_input("Chat input", label_visibility="collapsed", key="user_input", on_change=send_message)

    # Buttons for "Send" and "Reset Conversation"
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    st.button("Send", on_click=send_message)
    st.button("Reset Conversation", on_click=reset_conversation)
    st.markdown('</div>', unsafe_allow_html=True)

# Content for the "About Eliza" page
elif page == "About Eliza":
    st.markdown('<p style="font-family:Courier; color:white; font-size: 40px; text-align: center;">The Original ELIZA Chatbot</p>', unsafe_allow_html=True)
    st.markdown(
        """
        ELIZA was one of the first computer programs capable of natural language processing. It was created in the mid-1960s by **Joseph Weizenbaum**, a computer scientist at MIT. ELIZA used pattern matching and substitution methodology to simulate a conversation, giving users the illusion of interacting with a real psychotherapist.

        The most famous script implemented in ELIZA was called **DOCTOR**, which mimicked the conversational style of a Rogerian psychotherapist. ELIZA worked by identifying keywords and responding with pre-programmed phrases based on simple pattern recognition. Despite its limited understanding of human language, ELIZA demonstrated how computers could engage in conversations that appeared to be human-like, sparking significant interest in the field of Artificial Intelligence (AI).

        ELIZA's development was a breakthrough at the time and laid the foundation for future advancements in AI and natural language processing, inspiring the creation of more sophisticated chatbots and conversational agents.
        """
    )

# Content for the "Chat History" page
elif page == "Chat History":
    st.markdown('<p style="font-family:Courier; color:white; font-size: 40px; text-align: center;">Your Chat History with ELIZA</p>', unsafe_allow_html=True)

    if 'conversation' in st.session_state and st.session_state.conversation:
        for message in st.session_state.conversation:
            if message.startswith("You:"):
                st.markdown(f"<div class='chat-bubble user-message'>{message}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble eliza-message'>{message}</div>", unsafe_allow_html=True)
    else:
        st.write("No conversation history available.")

# Footer with name and website link
st.markdown(
    """
    <footer>
        Created by <a href="https://sainesh.com" target="_blank" style="color: #00BFFF; text-decoration: none;">Sainesh Nakra</a>
    </footer>
    """,
    unsafe_allow_html=True
)
