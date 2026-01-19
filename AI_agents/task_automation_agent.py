# Given a task list, decides execution sequence and performs dependent steps.

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import chromadb
from chromadb.utils import embedding_functions
import csv

load_dotenv()

client=chromadb.PersistentClient('../AI_agents/db_bin_files')
local_ef=embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

ids=[]
documents=[]
metadatas=[]

with open('TaskList.csv', mode='r') as tasks:
    reader=csv.DictReader(tasks, skipinitialspace=True)

    for i, row in enumerate(reader):
        ids.append(row['Task'])
    
        metadatas.append({
        "task name": row['Task Name'],
        "priority": row['Priority'],
        "status": row['Status'],
        "dependencies": row['Dependencies'] if row['Dependencies'] else "None"
        })

        text = (
            f"Task: {row['Task Name']}\n"
            f"Priority: {row['Priority']}\n"
            f"Status: {row['Status']}\n"
            f"Depends on: {row['Dependencies']}"
        )
     
        documents.append(text)

# Create collection in Chroma DB client
task_collection=client.get_or_create_collection(
    name="tasks",
    embedding_function=local_ef
)

# Data ingestion
task_collection.upsert(ids=ids, metadatas=metadatas, documents=documents)

# Operation to decide 'High' priority tasks that are left to be done
priority_value="High"
status_value="To Do"

query_strings= [
    f"I want to decide my task execution sequence, sort the tasks by {priority_value} and those that are left {status_value}"
]

# Executing query 
result = task_collection.query(
    query_texts=["List of important pending tasks"],
    n_results=5,
    where={
        "$and": [
            {"priority": {"$eq": "High"}},
            {"status": {"$eq": "To Do"}}
        ]
    }
)

llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
        )

context = "\n\n".join(result['documents'][0])

prompt = f"""
You are a project manager. Based on the following tasks (all High Priority and To Do), 
decide the correct execution sequence by looking at their dependencies.
Explain why you chose this order.

Tasks:
{context}
"""

response = llm.invoke(prompt)
print("LOGICAL EXECUTION SEQUENCE")
print(response.content)