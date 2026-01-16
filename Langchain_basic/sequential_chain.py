"""
Sequential processing in LangChain involves creating a pipeline of interconnected components 
(like prompt templates, models, and output parsers) 
where the output of one step automatically becomes the input for the next. 
This is ideal for breaking down complex tasks into smaller, manageable, and modular steps. 
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )

output_parser = StrOutputParser()

# Define prompt templates for each step
company_prompt = ChatPromptTemplate.from_template(
    "Generate a creative company name for a product that is {product}."
)

slogan_prompt = ChatPromptTemplate.from_template(
    "Write a catchy slogan for the company named {company_name}."
)

# Create the individual chains
company_chain = company_prompt | llm | output_parser
slogan_chain = slogan_prompt | llm | output_parser

# Combine them into a sequential workflow
full_chain = (
    {"company_name": company_chain} 
    | slogan_chain
)

# Invoke the chain
result = full_chain.invoke({"product": "colorful socks"})
print(result)