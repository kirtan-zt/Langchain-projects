"""
The RunnableBranch in LangChain is a core component of the LangChain Expression Language (LCEL)
that allows for conditional logic and routing within a chain, acting much like an if-elif-else statement. 

It enables developers to direct the flow of input to different sub-runnables (chains, models, functions, etc.) 
based on specific conditions, creating dynamic and adaptive AI workflows. 

"""


from langchain_core.runnables import RunnableBranch, RunnableLambda

# Define condition functions
is_string = lambda x: isinstance(x, str)
is_int = lambda x: isinstance(x, int)

# Define the runnables for each branch
string_branch = RunnableLambda(lambda x: x.upper())
int_branch = RunnableLambda(lambda x: x + 1)
default_branch = RunnableLambda(lambda x: "Not a string or int")

# Create the branch
branch = RunnableBranch(
    (is_string, string_branch),
    (is_int, int_branch),
    default_branch # The last item is the default
)

# Invoke with different inputs
print(branch.invoke("hello"))  
print(branch.invoke(59))     
print(branch.invoke(None))   