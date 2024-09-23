import streamlit as st

def clear_session_storage():
    st.session_state["Row"] = None
    st.session_state["Response"] = None
    st.session_state["Reprompt"] = False
    st.session_state["Re_Response"] = None

def pick_random_question():
    clear_session_storage()


st.title("OpenAI Prompting")
if st.button("Pick a random question 🎲"):
    row = pick_random_question()
    st.session_state["Row"] = row
