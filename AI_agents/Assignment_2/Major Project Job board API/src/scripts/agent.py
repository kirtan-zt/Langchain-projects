from langchain_classic.agents import AgentExecutor, create_react_agent
from src.core.config import settings
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from src.scripts.tools import vector_job_search, list_companies, list_jobs, list_resumes

# Define LLM
llm = init_chat_model(
    model=settings.LLM_MODEL,
    model_provider=settings.LLM_PROVIDER,
    api_key=settings.GROQ_API_KEY,
    temperature=0
)

# Define the toolset
tools = [vector_job_search, list_jobs, list_resumes, list_companies]

template = """
You are an intelligent Job Board Executive Agent. You have access to the system's database and vector search tools.
Solve the user's request by thinking step-by-step and using the tools provided. 

TOOLS:
------
You have access to the following tools:

{tools}

To use a tool, please use the following format:

Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (or "None" if no input is required)
Observation: the result of the action

(Repeat this Thought/Action/Observation loop as needed)

Thought: Do I need to use a tool? No
Final Answer: [your detailed response to the user]

USER REQUEST:
-------------
{input}

Thought: {agent_scratchpad}
"""

custom_prompt = PromptTemplate.from_template(template)

# Initialize the Agent
agent = create_react_agent(llm, tools, custom_prompt)

# Executor 
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors="Check your output format. Remember to use 'Final Answer:' when done.", 
)