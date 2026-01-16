Compliance Risk checker for Emails

### Title

An AI that analyzes outgoing business emails and warns if any risky or non-compliant communication is detected.

### Objective

Simulate a corporate email compliance assistant that checks if an outgoing mail violates legal, business, or internal guidelines.

**Expected Deliverables**

1.  User enters an email body as text.
    
2.  LangChain pipeline:
    
    1.  Evaluates the email
        
    2.  Detects possible risks such as promises, pricing mistakes, NDAs, confidential information, personal data, insults, legal commitments
        
3.  Output must contain:
    
    1.  Risk detected
        
    2.  Why it is a risk
        
    3.  Suggested alternative wording
        
4.  Provide a "severity rating" from 1 to 10.
    
5.  Optionally store user reports locally.
    

**Key LangChain Concepts Expected**

*   Evaluator chains
    
*   Custom prompt formatting
    
*   LLM output parsing
    
*   Decision scoring
    

**Required Tools**

*   Python
    
*   LangChain
    
*   LLM Provider OpenAI
    
*   CLI or Django form based UI
    

**Instructions to Complete**

*   Build a guided evaluator prompt.
    
*   Convert LLM output into structured risk analysis.
    
*   Provide improvement suggestions.
    
*   Test with multiple business emails.
    

**Success Criteria**

*   Output should be helpful, practical, and realistic.
    
*   Accuracy should improve based on refined prompts.