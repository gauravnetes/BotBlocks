import streamlit as st
import requests

st.set_page_config(
    page_title="Bot Builder",
    page_icon="🤖",
    layout="centered"
)

BACKEND_API_URL = "http://localhost:8000"

st.title("Welcome to Your Chatbot Builder 🤖")
st.markdown("Build and deploy your custom chatbot in minutes.")

st.divider()

st.header("1. Test Backend Connection")
st.markdown("Click the button to test the connection to your FastAPI backend.")

if st.button("Test Connection"):
    try:
        response = requests.get(f"{BACKEND_API_URL}/api/v1/health")

        if response.status_code == 200:
            backend_data = response.json()
            st.success(f"Connection Successful!")
            st.json(backend_data)
        else:
            st.error(f"Failed to connect. Status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Connection Failed!")
        st.warning(f"Could not connect to the backend at {BACKEND_API_URL}. Is it running?")
    except Exception as e:
        st.error(f"An unknown error occurred: {e}")