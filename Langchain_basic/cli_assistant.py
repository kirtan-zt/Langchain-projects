# Build a Command-Line Based AI Knowledge Assistant using LangChain
# Create a small AI assistant that can answer questions about a chosen topic 
# (example: Django, Python, AWS, company documentation) using LangChain.
"""
The assistant should:

Accept user questions in the command line
Send them to a selected LLM
Use LangChain core components (LLM, Prompt Template, Chains)
Return a well-structured answer
"""
import cmd
import os
import sys
import subprocess
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class knowledge_assistant(cmd.Cmd):
    intro = "Hello, I am your personal knowledge-assistant, ask me anything about a domain."
    prompt = "(user-query) "

    def __init__(self):
        super().__init__()
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY"),
            streaming=True
        )
        self.output_parser = StrOutputParser()

    def get_domain(self, question):
        """Internal helper to classify the domain of the question."""
        classifier_prompt = ChatPromptTemplate.from_template(
            "Identify the technical or general domain of this question: '{question}'. "
            "Return only the name of the domain (e.g., 'Django', 'Python', 'AWS'). "
            "Do not use full sentences."
        )
        classifier_chain = classifier_prompt | self.llm | self.output_parser
        return classifier_chain.invoke({"question": question}).strip()

    def default(self, line):
        """Take user's query to generate answers: ask <question>"""
        if not line:
            print("Please provide a question.")
            return

        try:
            detected_domain = self.get_domain(line)
            print(f"Detected Domain: {detected_domain}")

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", """You are an expert in {domain}. 
                    Provide a detailed answer and a confidence score in High/Medium/Low format."""),
                ("human", "{question}")
            ])
            
            chain = prompt_template | self.llm | self.output_parser

            for chunk in chain.stream({"domain": detected_domain, "question": line}):
                sys.stdout.write(chunk)
                sys.stdout.flush() 
            print("\n")
            
        except Exception as e:
            print(f"Error: {e}")

    def do_quit(self, line):
        """Exit the shell."""
        print("Goodbye, friend!")
        return True # exits the cmdloop

    # Handle the EOF character (Ctrl+D on Unix, Ctrl+Z on Windows) to exit
    def do_EOF(self, line):
        return self.do_quit(line)

if __name__ == "__main__":
    knowledge_assistant().cmdloop()
