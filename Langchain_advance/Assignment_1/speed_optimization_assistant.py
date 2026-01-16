import os
import requests
import json
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
import cmd

load_dotenv()

@tool
def get_reports(url: str) -> str:
    """
    Fetches Google PageSpeed Insights performance metrics for a specific URL.
    Input must be a valid URL string.
    """
    API_KEY = os.getenv('PAGESPEED_INSIGHTS_KEY')
    endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={API_KEY}&strategy=desktop"

    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        data = response.json()

        perf_score = data['lighthouseResult']['categories']['performance']['score'] * 100
        audits = data['lighthouseResult']['audits']
        
        # Extracting specific metrics
        fcp = audits['first-contentful-paint']['displayValue']
        lcp = audits['largest-contentful-paint']['displayValue']
        cls = audits['cumulative-layout-shift']['displayValue']
        tbt = audits['total-blocking-time']['displayValue']

        return (f"Score: {perf_score}\nFCP: {fcp}\nLCP: {lcp}\nCLS: {cls}\nTBT: {tbt}")
    except Exception as e:
        return f"Error: {str(e)}"

class SpeedOptimizationAssistant(cmd.Cmd):
    HISTORY_FILE = "audit_history.json"
    intro = "Welcome! Paste a URL to analyze performance, raw audit text or type 'history' to see past audits."
    prompt = "(AI-assistant) > "

    def __init__(self):
        super().__init__()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.tools = [get_reports]
        self.history = ChatMessageHistory()
        self.audit_history = self.load_history() 
        print(f"[*] Loaded {len(self.audit_history)} past reports.")
        
        
        self.prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Web Analytics Engineer. 
        LOGIC:
        1. If the user provides a URL ONLY, use the 'get_reports' tool.
        2. If the user provides raw metrics (from Lighthouse, GTMetrix, etc.), 
        analyze them directly without using any tools.
         
        When you provide your final answer, you MUST use this exact Markdown format:
        
        Optimization Report
        - Title: [Title]
        - Why it is required: [Reasoning]
        - Complexity: [Low/Medium/High]
        - Impact: [Expected Performance Gain]
        - Dev Notes: [Technical details]"""),
        
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
        
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt_template,
        )
        
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            )

    def load_history(self):
        """Loads history from a JSON file if it exists."""
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
        return []
    
    def save_history(self):
        """Saves current history to a JSON file."""
        try:
            with open(self.HISTORY_FILE, "w") as f:
                json.dump(self.audit_history, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")

    def default(self, line):
        """Processes the URL or Raw Audit text."""
        if not line:
            return

        print(f"\n Analyzing: {line}...")
        try:
            history_messages = self.history.messages
            result = self.agent_executor.invoke({"input": line, "chat_history": history_messages})
            output = result["output"]
            
            # Store in history
            self.audit_history.append({"input": line, "output": output})
            self.save_history()
            
            print(f"\n{output}\n")
            
        except Exception as e:
            print(f"Critial Error: {e}")

    def do_compare(self, line):
        """Compare the last two audits performed."""
        if len(self.audit_history) < 2:
            print("You need at least two audits in history to compare.")
            return

        # Get the last two entries
        site_a = self.audit_history[-2]['input']
        site_b = self.audit_history[-1]['input']

        query = f"Compare the performance of {site_a} and {site_b} based on the audits we just did. Create a comparison table."
        
        print(f"[*] Comparing {site_a} vs {site_b}...")
        try:
            result = self.agent_executor.invoke({
            "input": query,
            "chat_history": self.history.messages # This resolves the KeyError
            })
        
            print("\n" + result["output"] + "\n")

            self.history.add_user_message(query)
            self.history.add_ai_message(result["output"])
        
        except Exception as e:
            print(f"Error during comparison: {e}")

    def do_history(self, line):
        """View past audit summaries."""
        if not self.audit_history:
            print("No history found.")
            return
        for i, entry in enumerate(self.audit_history):
            print(f"Report #{i+1} for: {entry['input'][:50]}...")
            print(entry['output'])
            print("-" * 20)

    def do_quit(self, line):
        print("Goodbye!")
        return True

if __name__ == "__main__":
    SpeedOptimizationAssistant().cmdloop()