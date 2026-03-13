import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from src import TalentScoutBot, save_candidate, INITIAL_GREETING_TRIGGER

# Application Configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="💼",
    layout="centered",
)

# Custom UI Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("TalentScout")
    st.markdown("---")
    st.markdown(
        "Welcome to the **TalentScout Hiring Portal**. \n\n"
        "Our AI assistant is here to guide you through your initial screening. "
        "Please provide accurate information to help us match you with the best roles."
    )
    st.markdown("---")
    st.caption("© 2026 TalentScout Recruitment")

# Custom Main Header
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>TalentScout Hiring Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em;'>I'll walk you through a short screening interview to get your profile started.</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize Session State Variables
# 'bot': Persists the TalentScoutBot instance across Streamlit reruns
if "bot" not in st.session_state:
    st.session_state.bot = TalentScoutBot()

# 'interview_completed': Tracks whether the conversation has successfully concluded
if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False

# 'messages': Stores the chat history for display
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Trigger the first greeting message from the LLM
    initial_reply, _ = st.session_state.bot.get_response(
        INITIAL_GREETING_TRIGGER, chat_history=[]
    )
    st.session_state.messages.append(AIMessage(content=initial_reply))

# Render existing chat messages
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Handle UI state when the interview is over
if st.session_state.interview_completed:
    st.balloons()
    st.success(
        "Thank you for your time! Your profile has been submitted to the TalentScout team. "
        "We'll be in touch shortly."
    )
    # Allow the user to reset the session and start a new interview
    if st.button("Start New Interview"):
        del st.session_state.messages
        st.session_state.interview_completed = False
        st.rerun()

# Handle active interview interaction
else:
    # Capture user input from the chat box
    if user_input := st.chat_input("Type your response here…"):
        # Display the user's message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Snapshot the history *before* adding the current user message to pass into the LLM
        history_snapshot = st.session_state.messages.copy()
        st.session_state.messages.append(HumanMessage(content=user_input))

        # Generate and display the bot's response
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                reply, extracted_data = st.session_state.bot.get_response(
                    user_input, chat_history=history_snapshot
                )
            st.markdown(reply)

        st.session_state.messages.append(AIMessage(content=reply))

        # If data was extracted, the interview has concluded successfully
        if extracted_data:
            save_candidate(extracted_data)
            st.session_state.interview_completed = True
            st.rerun()
