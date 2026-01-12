# Query an LLM with unstructured text and receive strictly formatted JSON output.

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY=os.getenv("GROQ_API_KEY")

client=Groq()

query_text="""
    To the Billing Team, I’m Elena Rodriguez (elena.rod@designcorp.net). 
    I noticed a double charge on my last invoice (Invoice #88421) which shouldn't have happened. 
    I'd like to get the extra amount refunded to my card when you have a moment. 
    It isn't a rush, but I'd like it corrected before the next billing cycle.
    """

response=client.chat.completions.create(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    response_format={
        "type": "json_object"
    },
    messages=[
        {
            "role": "system",
            "content": """
                You are a helpful assistant designed to output JSON, kindly extract following fields from input:
                -User Name
                -Email
                -Issue summary
                -Urgency level (High, Medium, Low)
            """,
        },
        {
            "role": "user",
            "content": query_text
        }
    ]
)

print(response.choices[0].message.content)