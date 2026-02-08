import google.generativeai as genai
from .database import query_listings

# FIX: Use the 2026 stable model ID
# Options: "gemini-2.5-flash" (Recommended) or "gemini-3-flash-preview"
CURRENT_MODEL = "gemini-2.5-flash"

def generate_question(api_key):
    genai.configure(api_key=api_key)
    # Update to the latest model
    model = genai.GenerativeModel(CURRENT_MODEL)
    
    context = query_listings("property listing", api_key)
    if not context:
        return None, None

    prompt = f"Based on this listing: {context}\nGenerate ONE tricky real estate exam question."
    response = model.generate_content(prompt)
    return response.text, context

def evaluate_answer(user_answer, question, context, api_key):
    genai.configure(api_key=api_key)
    # Update to the latest model here too
    model = genai.GenerativeModel(CURRENT_MODEL)
    
    prompt = f"""
    Context: {context}
    Question: {question}
    Student Answer: {user_answer}
    
    Evaluate the student. If wrong, give a 'Deep Contextual Explanation' using details from 
    the listing. Explain the underlying real estate principle (Zoning, Law, or Finance).
    """
    return model.generate_content(prompt).text