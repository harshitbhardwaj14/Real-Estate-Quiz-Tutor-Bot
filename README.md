## 🚀 Setup & Tech Stack

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-000000?style=flat)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat)

### Tech Stack
- **Frontend:** Streamlit  
- **LLM:** Google Gemini 2.5 Flash  
- **Vector Database:** ChromaDB  
- **Embeddings:** `models/gemini-embedding-001`  
- **Language:** Python  

### Local Setup

```bash
# Clone the repository
git clone https://github.com/your-username/real-estate-ai-tutor.git
cd real-estate-ai-tutor

# Install dependencies
pip install -r requirements.txt

# Create Streamlit secrets file
mkdir .streamlit
echo 'GEMINI_API_KEY = "your_google_ai_studio_api_key"' > .streamlit/secrets.toml

# Run the application
streamlit run app.py

# App will be available at:
# http://localhost:8501

