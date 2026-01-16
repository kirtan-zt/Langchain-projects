from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2') 

def get_keywords(sentence):
    """Simple tokenizer to get unique lowercase words."""
    return set(sentence.lower().replace('.', '').split())

def calculate_keyword_similarity(sent1, sent2):
    """Calculates Jaccard Similarity (Intersection over Union)."""
    words1 = get_keywords(sent1)
    words2 = get_keywords(sent2)
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if len(union) > 0 else 0

def calculate_vector_similarity(sent1, sent2):
    """Existing Vector Similarity Logic."""
    emb1 = model.encode(sent1)
    emb2 = model.encode(sent2)
    return cosine_similarity([emb1], [emb2])[0][0]

# Test Case: High Semantic Similarity / Low Keyword Overlap
s1 = "The large dog ran quickly through the park"
s2 = "The big canine sprinted rapidly across the meadow."

kw_score = calculate_keyword_similarity(s1, s2)
vec_score = calculate_vector_similarity(s1, s2)

print(f"Sentence 1: {s1}")
print(f"Sentence 2: {s2}")
print("-" * 30)
print(f"Keyword Similarity (Jaccard): {kw_score:.4f}")
print(f"Vector Similarity (Cosine):  {vec_score:.4f}")