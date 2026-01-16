import cmd
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class ComplianceReport(BaseModel):
    risk_detected: str = Field(description="The specific risk areas found in the email")
    explanation: str = Field(description="Why this is a business or legal risk")
    alternative_wording: str = Field(description="A safer way to rephrase the context")
    severity_rating: float = Field(description="Rating from 1.0 to 10.0")

class email_risk_checker(cmd.Cmd):
    intro = "Hello, I am your corporate email compliance assistant, share a email body"
    prompt = "(Email-Body)"

    def __init__(self):
        super().__init__()
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
            streaming=True
        )
        self.parser = PydanticOutputParser(pydantic_object=ComplianceReport)
        self.analysis_prompt = ChatPromptTemplate.from_template(
            "System: You are a corporate compliance officer.\n"
            "Analyze the email for legal, business, or internal risks.\n"
            "Email Content: {email_body}\n\n"
            "{format_instructions}"
        ).partial(format_instructions=self.parser.get_format_instructions())

        self.chain = self.analysis_prompt | self.llm | self.parser

    def default(self, line):
        """Take user's query to detect risk threats"""
        if not line:
            print("Please provide a email body.")
            return

        try:
            # Evaluator Chain
            report = self.chain.invoke({"email_body": line})
            print("-"*20)
            print("According to my opinion, this is the report: \n")
            print(f"RISK DETECTED: {report.risk_detected}")
            print(f"SEVERITY: [{report.severity_rating}/10]")
            print(f"WHY: {report.explanation}")
            print(f"SUGGESTED: {report.alternative_wording}")
            print("-"*20)
            
        except Exception as e:
            print(f"Analysis Error: {e}")

    def do_quit(self, line):
        """Exit the shell."""
        print("Goodbye, friend!")
        return True # exits the cmdloop

    # Handle the EOF character 
    def do_EOF(self, line):
        return self.do_quit(line)

if __name__ == "__main__":
    email_risk_checker().cmdloop()