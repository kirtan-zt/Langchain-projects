import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os

# Initialize the Persistent Client 
client = chromadb.PersistentClient(path="./my_local_db")

# Load your data
df = pd.read_csv('arxiv_papers_5k.csv')
embeddings = np.load('embeddings_cohere_5k.npy')

model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare metadata
def prepare_metadata(df):
    """
    Prepare metadata for ChromaDB from our dataframe.

    Returns list of metadata dictionaries, one per paper.
    """
    metadatas = []

    for _, row in df.iterrows():
        # Extract year from published date (format: YYYY-MM-DD)
        year = int(str(row['published'])[:4])

        # Truncate authors if too long (ChromaDB has reasonable limits)
        authors = row['authors'][:200] if len(row['authors']) <= 200 else row['authors'][:197] + "..."

        metadata = {
            'title': row['title'],
            'category': row['category'],
            'year': year,  # Store as integer for range queries
            'authors': authors
        }
        metadatas.append(metadata)

    return metadatas

# Prepare metadata for all papers
metadatas = prepare_metadata(df)

# Check a sample
print("Sample metadata:")
print(metadatas[0])

try:
    client.delete_collection(name="arxiv_with_metadata")
    print("Deleted existing collection")
except Exception as e:
    pass  # Collection didn't exist, that's fine

# Create collection with metadata
collection = client.create_collection(
    name="arxiv_with_metadata",
    metadata={
        "description": "5000 arXiv papers with rich metadata for filtering",
        "hnsw:space": "cosine"  # Using cosine similarity
    }
)

print(f"Created collection: {collection.name}")

# Prepare data for insertion
ids = [f"paper_{i}" for i in range(len(df))]
documents = df['abstract'].tolist()

# Insert with metadata
# Our 5000 papers fit in one batch (limit is ~5,461)
print(f"Embedding {len(df)} papers with Hugging Face (MiniLM)...")

collection.add(
    ids=ids,
    documents=documents, 
    metadatas=metadatas
)

print(f"✓ Collection contains {collection.count()} papers with metadata")

# Create a helper function for queries
def search_with_filter(query_text, where_clause=None, n_results=5):
    """
    Search with optional metadata filtering.

    Args:
        query_text: The search query
        where_clause: Optional ChromaDB where clause for filtering
        n_results: Number of results to return

    Returns:
        Search results
    """
   
    query_embedding = model.encode(query_text, convert_to_numpy=True)

    # Search with optional filter
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        where=where_clause  # Apply metadata filter here
    )

    return results

# Example: Search for "deep learning optimization" only in ML papers
query = "deep learning optimization techniques"

results_filtered = search_with_filter(
    query,
    where_clause={"category": "cs.LG"}  # Only Machine Learning papers
)

print(f"Query: '{query}'")
print("Filter: category = 'cs.LG'")
print("\nTop 5 results:")
for i in range(len(results_filtered['ids'][0])):
    metadata = results_filtered['metadatas'][0][i]
    distance = results_filtered['distances'][0][i]

    print(f"\n{i+1}. {metadata['title']}")
    print(f"   Category: {metadata['category']} | Year: {metadata['year']}")
    print(f"   Distance: {distance:.4f}")

# Search for papers from 2024 or later
results_recent = search_with_filter(
    "neural network architectures",
    where_clause={"year": {"$gte": 2024}}  # Greater than or equal to 2024
)

print("Recent papers (2024+) about neural network architectures:")
for i in range(3):  # Show top 3
    metadata = results_recent['metadatas'][0][i]
    print(f"{i+1}. {metadata['title']} ({metadata['year']})")