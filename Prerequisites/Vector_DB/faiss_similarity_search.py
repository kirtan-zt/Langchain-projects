import faiss
import numpy as np

d = 64  # Dimension of the vectors

# Basic index that uses L2 (Euclidean) distance for search
index = faiss.IndexFlatL2(d)
print(f"Index is trained: {index.is_trained}") # For IndexFlatL2, this is True by default

nb = 1000  # Number of vectors in the database

# Generate 1000 random vectors of dimension 'd'
xb = np.random.random((nb, d)).astype('float32')

# Add the vectors to the index
index.add(xb)
print(f"Number of vectors in the index: {index.ntotal}")

nq = 1 # Number of query vectors
k = 8  # Number of nearest neighbors to retrieve

# Generate a random query vector
xq = np.random.random((nq, d)).astype('float32')

# Perform the search
distances, indices = index.search(xq, k)

print("Indices of nearest neighbors:", indices)
print("Distances to nearest neighbors:", distances)