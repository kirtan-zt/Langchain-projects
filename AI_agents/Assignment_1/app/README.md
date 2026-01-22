# Enterprise AI Knowledge Assistant
API documentation


## Document Routes
### 1. Upload document


```http
  POST /documents/upload
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `str` | **Required**. Name of the document
| `file`    | `UploadFile extension`   | Optional. Media upload (pdf)
| `text`      | `str` | Optional. Raw text if media not uploaded


Response:

```json
{
  "document_id": "62c57534-30b0-441d-8c49-24c40fb26e5c"
}
```

### 2. Retrieve documents
```http
  GET /documents/
```

Response:
```json
[
  {
    "id": "22559a37-e19b-45a6-b192-f360e1945d7d",
    "name": "company policy",
    "upload_date": "2026-01-19T08:56:38.631934Z"
  },
  {
    "id": "101637d5-9c4c-4c40-9ec0-2b5b02a8a531",
    "name": "KPMG employee policy",
    "upload_date": "2026-01-21T06:41:29.001722Z"
  }
]
```

### 3. Delete documents by document ID
```http
  DELETE /documents/{document_id}
```

Response:
```json
{
  "status": "deleted",
  "document_id": "62c57534-30b0-441d-8c49-24c40fb26e5c"
}
```

## Chatbot routes

### 1. List past chat conversation IDs and summary
```http
  GET /chats/
```

Response:
```json
[
  {
    "id": "7463c5b4-439c-49eb-a21f-d31fbb3757fa",
    "name": "Weekly Wage Increase Summary",
    "documents": []
  },
  {
    "id": "693ca190-c110-4c57-9bb1-3accec3da03f",
    "name": "Night Work Time Periods Defined",
    "documents": []
  }
]
```

### 2. Retrieve a specific HUMAN-AI conversation by chat ID with timestamp
```htttp
  GET /chats/{chat_id}/messages
```

Response:
```json
[
  {
    "id": "c06e1c8d-8699-468b-84da-c10fee9c4918",
    "chat_id": "7463c5b4-439c-49eb-a21f-d31fbb3757fa",
    "sender_type": "human",
    "content": "What are the Increase in wage per week € for whole-time employees?",
    "sources": null,
    "confidence": null,
    "created_at": "2026-01-21T06:43:08.109261Z"
  },
  {
    "id": "dde2f20b-4eff-4238-9f45-dcea7b07fb0b",
    "chat_id": "7463c5b4-439c-49eb-a21f-d31fbb3757fa",
    "sender_type": "ai",
    "content": "The increases in wage per week € for whole-time employees are as follows: \n1st January 2016: 1.75 per week, \n1st January 2015: 0.58 per week, \n1st January 2014: 3.49 per week, \n1st January 2013: 4.06 per week, \n1st January 2012: 4.66 per week \n(Source: KPMG employee policy, Page 5, Chunk 3 and KPMG employee policy, Page 5, Chunk 2)",
    "sources": [
      "KPMG employee policy – Page 5",
      "KPMG employee policy – Page 7",
      "KPMG employee policy – Page 10"
    ],
    "confidence": 1,
    "created_at": "2026-01-21T06:43:08.129428Z"
  }
]
```

### 3. Create a chat ID for one or multiple document IDs
```http
  POST /chats/
```

Body:
```json
{
  "document_ids": [
    "101637d5-9c4c-4c40-9ec0-2b5b02a8a531"
  ]
}
```

Response:
```json
{
  "id": "225c20ba-f195-4592-9a04-161e166fe624",
  "name": "New Chat",
  "documents": []
}
```

Error Handling: Chat ID is only created for uploaded document IDs

Body (some random document id that is not in database)
```json
{
  "document_ids": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ]
}
```

Response:
```json
{
  "detail": "One or more document_ids are invalid"
}
```

### 4. Send message using the chat ID to AI model for getting Response
```http
  POST /chats/{chat_id}/messages
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `chat id`      | `UUID` | **Required**. Unique chat_id mapped to document_id

Body:
```json
{
  "content": "What are the time periods allocated in Night Work?"
}
```

Response:
```json
{
  "answer": "According to the KPMG employee policy (Page 6, Chunk 1 and Page 6, Chunk 0), the time periods allocated in Night Work are:\n- Night time: between 10 p.m. of any one day and 6 a.m. of the next day.\n- A night worker's normal hours of work: must not exceed an average of eight hours in any twenty-four hour period.\n- Reference period: seventeen weeks in the course of employment.\n- Minimum weekly rest period: twenty-four hours.\n\nSources: \n- KPMG employee policy, Page 6, Chunk 1\n- KPMG employee policy, Page 6, Chunk 0",
  "references": [
    "KPMG employee policy – Page 6",
    "KPMG employee policy – Page 8"
  ],
  "confidence": 1
}
```

Body: (Test conversation memory)
- Question-1:
```json
{
  "content": "What is the notice period under termination?"
}
```

Response:
```json
{
  "answer": "The notice periods vary depending on the length of employment the employee has been with the same employer continuously. \nAccording to the policy (KPMG employee policy, Page 4, Chunk 5), the notice periods are as follows:\n- for more than one month but not more than six months: one week\n- for more than six months but not more than two years: two weeks\n- for more than two years but not more than four years: four weeks.\n\nAdditionally, if an employee fails to give notice, they are liable to pay the employer a sum equal to half the wages that would be payable in respect of the period of notice (KPMG employee policy, Page 4, Chunk 4). \n\nSources: \n- KPMG employee policy, Page 4, Chunk 5\n- KPMG employee policy, Page 4, Chunk 4",
  "references": [
    "KPMG employee policy – Page 8",
    "KPMG employee policy – Page 4"
  ],
  "confidence": 1
}

```
- Question-2: follow-up Question
Body: 
```json
{
  "content": "What about senior managers?"
}
```

Response:
```json
{
  "answer": "According to the policy (KPMG employee policy, Page 4, Chunk 6), for technical, administrative, executive or managerial posts, the notice period may be such longer periods as may be agreed by the employer and employee.\n\nSource: \n- KPMG employee policy, Page 4, Chunk 6",
  "references": [
    "KPMG employee policy – Page 6",
    "KPMG employee policy – Page 11",
    "KPMG employee policy – Page 13",
    "KPMG employee policy – Page 4"
  ],
  "confidence": 1
}
```

## Log History Routes to fetch all conversations

### List all message logs
```http
  GET /logs/
```

Response:
```json
[
  {
    "id": "1dd948c6-6ed3-4b71-87f4-e1b43d6cf167",
    "chat_id": "8530fee5-8121-4f3b-ab8e-da834cc6deec",
    "sender_type": "ai",
    "content": "According to [Source: KPMG employee policy, Page 6, Chunk 2], when there is a change in working environment, it is the duty of the employer to ensure the employee concerned undergoes a health assessment. \n\nAdditionally, [Source: KPMG employee policy, Page 11, Chunk 0] and [Source: KPMG employee policy, Page 11, Chunk 1] outline the employer's duties to ensure health and safety at all times, but the specific mention of a change in working environment is found in [Source: KPMG employee policy, Page 6, Chunk 2]. \n\nSources: \n- KPMG employee policy, Page 6, Chunk 2\n- KPMG employee policy, Page 11, Chunk 0\n- KPMG employee policy, Page 11, Chunk 1",
    "sources": [
      "KPMG employee policy – Page 6",
      "KPMG employee policy – Page 11",
      "KPMG employee policy – Page 2"
    ],
    "confidence": 1,
    "created_at": "2026-01-22T10:04:58.314713Z"
  },
  {
    "id": "84b5928e-0d81-4614-8ee4-cefbcf091630",
    "chat_id": "8530fee5-8121-4f3b-ab8e-da834cc6deec",
    "sender_type": "human",
    "content": "What is the duty of employer to be carried out when there is a change in working environment?",
    "sources": null,
    "confidence": null,
    "created_at": "2026-01-22T10:04:58.309973Z"
  },
  {
    "id": "6d65d2e5-4334-4e5b-926a-1ed187de020b",
    "chat_id": "693ca190-c110-4c57-9bb1-3accec3da03f",
    "sender_type": "ai",
    "content": "According to the KPMG employee policy (Page 6, Chunk 1 and Page 6, Chunk 0), the time periods allocated in Night Work are:\n- Night time: between 10 p.m. of any one day and 6 a.m. of the next day.\n- A night worker's normal hours of work: must not exceed an average of eight hours in any twenty-four hour period.\n- Reference period: seventeen weeks in the course of employment.\n- Minimum weekly rest period: twenty-four hours.\n\nSources: \n- KPMG employee policy, Page 6, Chunk 1\n- KPMG employee policy, Page 6, Chunk 0",
    "sources": [
      "KPMG employee policy – Page 8",
      "KPMG employee policy – Page 6"
    ],
    "confidence": 1,
    "created_at": "2026-01-21T06:46:43.275908Z"
  },
  {
    "id": "11c39009-980f-4159-b53e-dfa5e7d05744",
    "chat_id": "693ca190-c110-4c57-9bb1-3accec3da03f",
    "sender_type": "human",
    "content": "What are the time periods allocated in Night Work?",
    "sources": null,
    "confidence": null,
    "created_at": "2026-01-21T06:46:43.246902Z"
  }
]
```