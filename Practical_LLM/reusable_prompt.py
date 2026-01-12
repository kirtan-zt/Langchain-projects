"""
Create a template with sections:

System instruction
Task instruction
Context placeholder
Output format (JSON or YAML example)
"""

from langchain_core.prompts import ChatPromptTemplate

# Define the Standardized Template
template = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "You are an expert in {domain}. Your task is to extract key entities "
            "and transform them into a structured {output_language} format. "
            "Do not include conversational filler; return ONLY the structured data."
        ),
        (
            "human", 
            "CONTEXT\n{context}\n\n"
            "TASK\n{task_instruction}\n\n"
            "OUTPUT FORMAT\n"
            "Produce the result as {output_language} following this structure:\n"
            "{format_example}"
        ),
    ]
)

# Invoke with specific data
prompt = template.invoke(
    {
        "domain": "Information Security",
        "context": "Enterprise Cybersecurity",
        "task_instruction": "Extract definitions for Threat, Vulnerability, and Risk.",
        "output_language": "JSON",
        "format_example": '{"term": "definition"}'
    }
)

print(prompt.to_string())