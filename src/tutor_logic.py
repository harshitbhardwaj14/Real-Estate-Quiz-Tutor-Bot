import google.generativeai as genai
from .database import query_listings

# 2026 Stable Model Alias
CURRENT_MODEL = "gemini-2.5-flash"

def generate_question(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(CURRENT_MODEL)
    
    # Randomly pull a property to quiz on
    context = query_listings("property listing", api_key)
    if not context:
        return None, None, None

    # THE ENHANCED PROMPT: Prevents leaking and handles edge cases
    prompt = f"""
    SYSTEM: You are a Real Estate Licensing Exam Proctor. 
    CONTEXT: {context}
    
    TASK: Generate 1 tricky Multiple Choice Question (MCQ).
    
    EDGE CASE RULES:
    - If the context is missing price or zoning, focus on the property description.
    - Do NOT mention the answer in the first section.
    - Create 4 plausible options (A, B, C, D).
    
    OUTPUT FORMAT (STRICT):
    [Question and Options]
    |||
    [Correct Letter Only]
    |||
    [Brief Explanation of the correct legal principle]
    """
    
    response = model.generate_content(prompt)
    parts = response.text.split("|||")
    
    if len(parts) >= 3:
        return parts[0].strip(), parts[1].strip(), parts[2].strip()
    return response.text, "N/A", "N/A"

def evaluate_answer(user_answer, correct_letter, explanation, api_key):
    """
    Simplified evaluation: compares user input to the 'secret' correct letter.
    """
    is_correct = user_answer.strip().upper() == correct_letter.strip().upper()
    feedback = "✅ **Correct!**" if is_correct else f"❌ **Incorrect. The correct answer was {correct_letter}.**"
    return f"{feedback}\n\n**Legal Insight:** {explanation}"