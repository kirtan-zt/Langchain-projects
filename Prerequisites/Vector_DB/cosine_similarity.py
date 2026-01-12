# Store embeddings in a list and compute cosine similarity manually (concept-level).

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2') 

def compute_embedding(sentence):
 """Get embeddings for your texts (e.g., documents, sentences)"""
 embedding = model.encode(sentence)
 return embedding

def calculate_similarity(embedding1, embedding2):
 """Calculating Cosine Similarity:"""
 similarity = cosine_similarity([embedding1], [embedding2])[0][0]
 return similarity

sentence1 = "The prime minister of India is Narendra Modi."
sentence2 = "The prime minister of USA is Donald Trump."

embedding1 = compute_embedding(sentence1)
embedding2 = compute_embedding(sentence2)

similarity_score = calculate_similarity(embedding1, embedding2)
print("Sentence 1:", sentence1)
print("Sentence 2:", sentence2)
print("Cosine Similarity Score:", similarity_score)