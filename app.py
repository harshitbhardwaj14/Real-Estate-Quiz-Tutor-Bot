import streamlit as st
import json
from src.database import process_and_store_json
from src.tutor_logic import generate_question, evaluate_answer

st.set_page_config(page_title="Real Estate Tutor", layout="wide")

# API Key Setup
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.warning("Please provide an API Key.")
    st.stop()

# Ingestion
st.sidebar.title("Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Listings (JSON)", type="json")
if uploaded_file:
    data = json.load(uploaded_file)
    count = process_and_store_json(data, api_key)
    st.sidebar.success(f"Indexed {count} properties.")

# Quiz Logic
st.title("🏡 Real Estate AI Tutor")
if st.button("Generate New Question"):
    q, ctx = generate_question(api_key)
    st.session_state.q, st.session_state.ctx = q, ctx

if "q" in st.session_state and st.session_state.q:
    st.info(f"**Scenario:** {st.session_state.ctx}")
    st.subheader(st.session_state.q)
    ans = st.text_area("Your response:")
    if st.button("Submit"):
        feedback = evaluate_answer(ans, st.session_state.q, st.session_state.ctx, api_key)
        st.write(feedback)