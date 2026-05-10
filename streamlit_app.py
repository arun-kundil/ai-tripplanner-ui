import streamlit as st
import datetime
import requests
import sys

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon=":airplane:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("AI Trip Planner")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("How can I assist you with your travel plans today? Let me know your destination")


with st.form():
    user_input = st.text_input("User Input", placeholder="e.g. Plan a trip to Paris for 5 days in September")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:
        # Show user message
        # Show thinking spinner while backend processes the request
        with st.spinner("Planning your trip..."):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "Sorry, I couldn't get a response.")
            markdown_content = f"""# :airplane: Your AI-Generated Travel Plan :airplane:
            # **Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**
            # **Created by :** Arun's AI Trip Planner
            ---
            {answer}
            ---
            *This travel plan was generated using the latest real-time data and insights to help you have the best travel experience possible. Always double-check details and make reservations in advance!*
            """

            st.markdown(markdown_content)
        else:
            st.error("Sorry, there was an error processing your request. Please try again later.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
