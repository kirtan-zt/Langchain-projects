#  Best practices-1: Always normalise vectors when using cosine similarity

import numpy as np
from numpy.linalg import norm

vector_a = np.array([1, 2, 3])
vector_b = np.array([4, 5, 6])

# Normalize vectors
norm_a = norm(vector_a)
norm_b = norm(vector_b)

normalized_a = vector_a / norm_a
normalized_b = vector_b / norm_b

# Calculate cosine similarity (dot product of normalized vectors)
cosine_sim = np.dot(normalized_a, normalized_b)

print(f"Normalized Vector A: {normalized_a}")
print(f"Normalized Vector B: {normalized_b}")
print(f"Cosine Similarity: {cosine_sim}")
