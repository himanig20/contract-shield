import numpy as np
import streamlit as st

@st.cache_resource
def load_nlp_model():
    """
    Loads the sentence-transformers model.
    Cached by Streamlit so it only downloads/loads into RAM once per session.
    """
    try:
        from sentence_transformers import SentenceTransformer
        print("Loading NLP Model: all-MiniLM-L6-v2 ...")
        # all-MiniLM-L6-v2 is very small (80MB) and fast for this purpose
        model = SentenceTransformer('all-MiniLM-L6-v2') 
        return model
    except Exception as e:
        print(f"Failed to load sentence_transformers: {e}")
        return None

@st.cache_data
def get_anchor_embeddings(anchors_tuple):
    """
    Caches the embeddings of our reference anchors so they aren't generated repeatedly.
    """
    model = load_nlp_model()
    if model is None:
        return None
    return model.encode(list(anchors_tuple))

def compute_similarity(clause_text, anchors, model):
    """
    Computes max cosine similarity between a clause and a list of anchor sentences.
    """
    if not model or not anchors:
        return 0.0
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Generate embedding for the new user string
    clause_embedding = model.encode([clause_text])
    
    # Fetch cached embeddings for the rule's anchor strings
    anchor_embeddings = get_anchor_embeddings(tuple(anchors))
    
    # Calculate cosine similarities
    similarities = cosine_similarity(clause_embedding, anchor_embeddings)[0]
    
    # Return the highest similarity score matched against any anchor
    return float(np.max(similarities))
