import chromadb
import google.generativeai as genai
import streamlit as st
from chromadb.utils import embedding_functions


# --- 2026 Stable Model Configuration ---
# 'models/gemini-embedding-001' is the universally supported ID for v1beta in 2026
MODEL_NAME = "models/gemini-embedding-001"
DB_PATH = "./data/chroma_db"

def get_collection(api_key):
    """Initializes and returns ChromaDB collection with Gemini embeddings."""
    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=api_key,
        model_name=MODEL_NAME
    )
    
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name="real_estate_tutor_v2",
        embedding_function=gemini_ef
    )

def process_and_store_json(json_data, api_key):
    """Processes property JSON data and stores it in ChromaDB."""
    if not isinstance(json_data, list):
        st.error("Invalid JSON: Data must be a list of property objects.")
        return 0
    
    collection = get_collection(api_key)
    docs, metadatas, ids = [], [], []

    for i, item in enumerate(json_data):
        if not isinstance(item, dict):
            continue
        
        address = item.get('address', 'Unknown Address')
        desc_text = item.get('description', '')
        price = item.get('price', 'N/A')
        
        combined_text = f"Address: {address} | Price: {price} | Description: {desc_text}"
        
        docs.append(combined_text)
        metadatas.append({str(k): str(v) for k, v in item.items()})
        ids.append(str(item.get('id', f"prop_{i}")))

    if docs:
        try:
            collection.upsert(documents=docs, metadatas=metadatas, ids=ids)
            return len(docs)
        except Exception as e:
            st.error(f"Critical Error during storage: {e}")
            return 0
    return 0

def query_listings(query_text, api_key):
    """Queries database for most relevant property matching query."""
    try:
        collection = get_collection(api_key)
        results = collection.query(query_texts=[query_text], n_results=1)
        if results and results['documents']:
            return results["documents"][0][0]
    except Exception:
        return None
    return None
