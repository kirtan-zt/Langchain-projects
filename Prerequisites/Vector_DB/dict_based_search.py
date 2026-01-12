# Create a simple dictionary-based search mechanism to mimic vector retrieval.

from sentence_transformers import SentenceTransformer

words=["Cat", "Dog", "Sofa", "Coffee", "Table", "Car"]

word_embeddings = {}  # Creating an empty dictionary to map words with their embedding value

model = SentenceTransformer('all-MiniLM-L6-v2') 

embedding=model.encode(words)

for key, value in zip(words, embedding):
    word_embeddings[key]=value

print(word_embeddings) # Printing the entire dictionary of word-embedding pairs
print(f"Cat embedding value={word_embeddings["Cat"]}") # Dict-based search mechanism