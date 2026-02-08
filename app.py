import streamlit as st
import json
from src.database import process_and_store_json
from src.tutor_logic import generate_question, evaluate_answer

st.set_page_config(page_title="Real Estate Tutor 2026", layout="wide")

# API Key Check
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
    st.info("Enter API Key to start.")
    st.stop()

# Sidebar Data Management
st.sidebar.header("Admin")
uploaded_file = st.sidebar.file_uploader("Upload Listings (JSON)", type="json")
if uploaded_file:
    data = json.load(uploaded_file)
    count = process_and_store_json(data, api_key)
    st.sidebar.success(f"Indexed {count} properties.")

# Main Tutor Interface
st.title("🏡 Real Estate Exam Prep")

if st.button("Get New Question"):
    # Clear old state
    for key in ['q', 'ans', 'expl', 'submitted']:
        if key in st.session_state: del st.session_state[key]
        
    q, ans, expl = generate_question(api_key)
    st.session_state.q = q
    st.session_state.ans = ans
    st.session_state.expl = expl

if "q" in st.session_state:
    st.markdown("### Test Your Knowledge")
    st.markdown(st.session_state.q)
    
    user_choice = st.radio("Choose the best option:", ["A", "B", "C", "D"], key="user_choice")
    
    if st.button("Submit Answer"):
        st.session_state.submitted = True
        
    if st.session_state.get("submitted"):
        result = evaluate_answer(user_choice, st.session_state.ans, st.session_state.expl, api_key)
        st.write(result)