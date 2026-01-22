## AI Responses

## Vector embeddings usage

### 1) Sync Job Listings by ID

Method: POST

Request URL: http://127.0.0.1:8000/sync/listings/6

Response:

```json
{
  "status": "success",
  "message": "Embedding synced for: Database administrator"
}
```

### 2) Trigger Sync for new entries into vector DB

Method: POST

Request URL: http://127.0.0.1:8000/ai/sync-embeddings

Response:

```json
{
  "status": "success",
  "synced_records": 6
}
```

### 3) Recommendations that match with profile

Method: POST

Request URL: http://127.0.0.1:8000/ai/recommend

Body:

```json
{
  "resume_text": "My skill set include proficiency in core languages (HTML, CSS, JavaScript) and frameworks such as React. Recommend jobs from the portal for my profile."
}
```

Response:

```json
{
  "status": "success",
  "recommendations": [
    {
      "job_title": "Senior Frontend Developer",
      "match_reason": "The candidate's proficiency in core languages (HTML, CSS, JavaScript) and frameworks such as React matches the job requirements of expert-level knowledge of JavaScript, HTML5, and CSS3, including proficiency in modern frameworks like React.",
      "confidence_score": 90
    }
  ]
}
```

### 4) Improve raw job description for recruiters to improve clarity, grammar, SEO keyword richness

Method: POST

Select improvement modes from ENUM:

- SHORT AND CRISP
- DETAILED AND FORMAL
- MARKETING ORIENTED

Request URL: http://127.0.0.1:8000/ai/improve-description?mode=DETAILED AND FORMAL

Body:

```json
{
  "text": "we looking for someone who can code good. job is for full stack developer but mostly doing python and react. you must know how to make website work and fix bugs when they break. we use databases like sql and mongo sometimes. we are a fast company and need you to start fast. no time for slow people. must have 3 years doing this. we offer money and some benefits. send resume if u want it."
}
```

Response:

```json
{
  "status": "success",
  "data": {
    "improved_description": "We are seeking a highly skilled Full Stack Developer to join our dynamic team. The ideal candidate will have a strong proficiency in Python and React, with a proven track record of developing and maintaining complex web applications. The successful candidate will be responsible for ensuring the seamless functionality of our websites, troubleshooting and resolving bugs, and collaborating with our team to drive project delivery. Experience with databases such as SQL and MongoDB is also essential. As a fast-paced company, we require a candidate who can hit the ground running and make an immediate impact. A minimum of 3 years of experience in a similar role is required. In return, we offer a competitive salary and a range of benefits. If you are a motivated and talented developer looking for a new challenge, please submit your resume for consideration.",
    "clarity_improvements": "Reorganized the job description to clearly outline the key responsibilities and requirements of the role, ensuring that candidates understand the expectations and can accurately assess their suitability. Removed ambiguous language and phrases to improve overall clarity.",
    "grammar_fixes": "Corrected numerous grammatical errors, including verb tense inconsistencies, missing articles, and incorrect punctuation. Improved sentence structure to enhance readability and flow.",
    "professionalism_score": "The rewritten job description demonstrates a significant improvement in professionalism, with a score of 9 out of 10. The tone is now formal and polished, making it more attractive to high-caliber candidates.",
    "seo_keywords_added": [
      "Full Stack Developer",
      "Python",
      "React",
      "Web Development",
      "Database Management",
      "SQL",
      "MongoDB",
      "Job Opportunity",
      "Career Search"
    ]
  }
}
```

## Demonstration of Agent Executor chain

Testing AI-agent with a question and check the terminal response:

```bash
  Find out job listings that offer Hybrid mode of work and the salary range is more than 3L
```

```bash
> Entering new AgentExecutor chain...
Thought: Do I need to use a tool? Yes
Action: vector_job_search
Action Input: "Hybrid mode of work" and "salary range more than 3L"Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefully

Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)Thought: The observation from the previous action provides some job listings that offer Hybrid mode of work, but it does not explicitly mention the salary range for each job listing. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to filter the results based on the salary range.

Action: vector_job_search
Action Input: "Hybrid mode of work" and "salary range more than 3L" and "job listings with salary information"Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefully

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)Thought: The observation from the previous action still does not provide the salary range for each job listing. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to use a different approach. I can try to list all the jobs and then filter the results based on the location and salary range.

Action: list_jobs
Action Input: NoneINFO:     Request for POST method started
INFO:     Response for POST method completed with status code 200 in 0.35s
INFO:     127.0.0.1:50924 - "POST /users/login HTTP/1.1" 200 OK
INFO:     Request for GET method started
INFO:     Response for GET method completed with status code 200 in 0.07s
INFO:     127.0.0.1:50926 - "GET /listings/ HTTP/1.1" 200 OK
[{"listing_id": 6, "title": "Database administrator", "Type of work": "Part-Time", "Status": "Still accepting"}, {"listing_id": 7, "title": "Mechanical design engineer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 8, "title": "Senior Frontend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 9, "title": "Senior Backend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 10, "title": "Lead Maintenance Engineer", "Type of work": "Full-Time", "Status": "Still accepting"}]Thought: The observation from the previous action provides a list of job listings, but it does not include information about the location or salary range. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to use a different approach. I can try to use the vector_job_search tool with a more specific query that includes the salary range.

Action: vector_job_search
Action Input: "Hybrid mode of work" and "salary range more than 3L" and "job listings with salary information"Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefully

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)Thought: It seems that the previous actions did not provide the desired results. The vector_job_search tool is not able to provide job listings with salary information. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to think of a different approach.

Action: list_jobs
Action Input: NoneINFO:     Request for GET method started
INFO:     Response for GET method completed with status code 200 in 0.01s
INFO:     127.0.0.1:50928 - "GET /listings/ HTTP/1.1" 200 OK
[{"listing_id": 6, "title": "Database administrator", "Type of work": "Part-Time", "Status": "Still accepting"}, {"listing_id": 7, "title": "Mechanical design engineer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 8, "title": "Senior Frontend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 9, "title": "Senior Backend Developer", "Type of work": "Full-Time", "Status": "Still accepting"}, {"listing_id": 10, "title": "Lead Maintenance Engineer", "Type of work": "Full-Time", "Status": "Still accepting"}]Thought: It seems that the previous actions did not provide the desired results. The vector_job_search tool is not able to provide job listings with salary information, and the list_jobs tool does not provide information about the location or salary range. To find job listings that offer Hybrid mode of work and a salary range of more than 3L, I need to think of a different approach.

Since the tools provided do not seem to be able to provide the desired results, I will try to analyze the observations from the previous actions. From the observations, I can see that there are some job listings that offer Hybrid mode of work, but the salary range is not explicitly mentioned.

Action: list_companies
Action Input: NoneINFO:     Request for GET method started
INFO:     Response for GET method completed with status code 200 in 0.03s
INFO:     127.0.0.1:50929 - "GET /companies/ HTTP/1.1" 200 OK
[{"Company name": "Google LLC", "ID": 11, "Industry": "Information Technology"}, {"Company name": "Reliance Industries Limited (RIL)", "ID": 13, "Industry": "Chemical"}]Thought: Based on the observations from the previous actions, I can see that there are some job listings that offer Hybrid mode of work, but the salary range is not explicitly mentioned. I can try to analyze the job listings that offer Hybrid mode of work and see if I can find any information about the salary range.

Action: vector_job_search
Action Input: "Hybrid mode of work" and "job listings with salary information"Role: Business Analyst. Company: Google LLC. Location: modes.hybrid. Details: Act as a liaison between business teams, IT, and management, translating needs and validating requirements, Support the design of technical solutions and participate in Quality Assurance (QA) and User Acceptance Testing (UAT).

Role: Senior Backend Developer. Company: Google LLC. Location: modes.hybrid. Details: Strong proficiency in backend languages (e.g., Python, Java, Node.js, C#), Experience with frameworks (e.g., Spring Boot, Express, Django) and DevOps tools (Docker, Kubernetes)

Role: Mechanical design engineer. Company: Reliance Industries Limited (RIL). Location: modes.on_site. Details: A candidate who has the potential to carry out successful 3D design of a thermal power plant and manage resources carefullyThought: Based on the observations from the previous actions, I can see that there are some job listings that offer Hybrid mode of work, but the salary range is not explicitly mentioned. However, I can try to analyze the job listings that offer Hybrid mode of work and see if I can find any information about the salary range.

From the observations, I can see that the job listings that offer Hybrid mode of work are from companies such as Google LLC. Based on industry standards and market trends, I can infer that the salary range for these job listings is likely to be more than 3L.

Action: None
Final Answer: Based on the analysis of the job listings that offer Hybrid mode of work, I can provide the following job listings that are likely to have a salary range of more than 3L:

1. Business Analyst at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.
2. Senior Backend Developer at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.

Please note that the salary range is not explicitly mentioned in the job listings, and the inference is based on industry standards and market trends. It is recommended to contact the companies directly to confirm the salary range for these job listings.

> Finished chain.
INFO:     Response for POST method completed with status code 200 in 13.85s
INFO:     127.0.0.1:50922 - "POST /ai/ask-agent?query=Find%20out%20job%20listings%20that%20offer%20Hybrid%20mode%20of%20work%20and%20the%20salary%20range%20is%20more%20than%203L HTTP/1.1" 200 OK
```

### Response body output

```json
{
  "status": "success",
  "output": "Based on the analysis of the job listings that offer Hybrid mode of work, I can provide the following job listings that are likely to have a salary range of more than 3L:\n\n1. Business Analyst at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.\n2. Senior Backend Developer at Google LLC - This job listing offers Hybrid mode of work and is likely to have a salary range of more than 3L based on industry standards and market trends.\n\nPlease note that the salary range is not explicitly mentioned in the job listings, and the inference is based on industry standards and market trends. It is recommended to contact the companies directly to confirm the salary range for these job listings."
}
```

### Testing the AI Agent with irrelevant questions

```bash
What is the weather in California today?
```

```bash
> Entering new AgentExecutor chain...
Thought: Do I need to use a tool? No
The tools provided are related to job searching and recruitment, and none of them seem to be relevant to checking the weather in California.

Final Answer: I'm afraid I'm a Job Board Executive Agent and do not have access to real-time weather information. However, I can suggest checking a weather website or app, such as AccuWeather or Weather.com, for the current weather in California. If you have any job-related questions or need assistance with finding a job, I'd be happy to help!

> Finished chain.
INFO:     Response for POST method completed with status code 200 in 0.77s
```

### Response body output

```json
{
  "status": "success",
  "output": "I'm afraid I'm a Job Board Executive Agent and do not have access to real-time weather information. However, I can suggest checking a weather website or app, such as AccuWeather or Weather.com, for the current weather in California. If you have any job-related questions or need assistance with finding a job, I'd be happy to help!"
}
```
