SaaS Speed Optimization Assistant

### Title

AI Tool that analyzes a website performance report and proposes optimization actions.

### Objective

Build an internal AI tool that allows a user to upload or paste a website speed audit report (Lighthouse, GTMetrix, PageSpeed, etc.) and generates prioritized technical optimization recommendations with impact scores and estimated development effort.

**Expected Deliverables**

1.  User can input or paste raw audit text into the system.
    
2.  System parses the input and extracts meaningful insights using LangChain processing tools.
    
3.  System returns structured recommendations including:
    
    1.  Title of optimization
        
    2.  Why it is required
        
    3.  Estimated complexity (Low, Medium, High)
        
    4.  Expected performance impact
        
    5.  Additional developer notes
        
4.  User can run multiple audits and compare outputs.
    
5.  Logs or stored history of past reports for reference.
    

**Key LangChain Concepts Expected**

*   Tool usage
    
*   Prompt templates
    
*   Custom parsing chain
    
*   Output structuring
    
*   Memory handling
    
*   Flow orchestration
    

**Tools and Technologies**

*   Python
    
*   LangChain
    
*   OpenAI LLM
    
*   Django or Python CLI app
    

**Instructions to Complete**

*   Receive raw audit report from user.
    
*   Build a prompt template that instructs the model to extract performance issues and convert them into actionable tasks.
    
*   Create the LangChain execution pipeline.
    
*   Present structured results back to the user.
    
*   Implement basic local storage for historical reports (JSON or DB).
    

**Success Criteria**

*   Outputs should be consistent, clear, human usable, and repeatable.
    
*   Tool should handle messy input but still generate structured results.
    
*   Recommendations should feel like real production output.