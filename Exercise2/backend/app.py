from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel
from rag import fetch_chroma_data, retrieve_context, load_schema_and_samples,embed_and_store_feedback, load_feedback_into_rag
from mysql_db_utils import get_connection
import ollama
import uvicorn
import os


OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral-small:latest')

conn = get_connection()

load_schema_and_samples(conn)
load_feedback_into_rag()

app = FastAPI()

class Questions(BaseModel):
    question: str
    
class Feedback(BaseModel):
    question: str
    approved_sql: str

@app.post("/query")
def answer_query(q: Questions):
    context = retrieve_context(q.question)
    prompt = f"""
You are an expert MySQL developer. Given the following database context and a natural language question,
generate a safe, syntactically correct, and precise MySQL query. Use only the tables and columns that are relevant.
Never delete or modify data. Only generate SELECT queries.

Context:\n{context}
Question:\n{q.question}
Write only the MySQL query no need to add any extra word or quote before and after query
If user's question is not related to datbase provided answer with "I'm a text-to-SQL model, not your Tinder wingman. If you want a query, I got you. If you're lonely, call your ex or your DBA.":
"""
    ollama_client = ollama.Client(host=OLLAMA_URL)
    response = ollama_client.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
    sql_query = response['message']['content'].strip()
    print(f"response from ollama : {sql_query}")
    trimmed_sql_query = sql_query.replace('\n', ' ')
    print(sql_query)
    return {"query": trimmed_sql_query}


@app.get("/fetch")
def fetch(doc_id: Optional[str] = Query(None, description="Document ID to fetch")):
    return fetch_chroma_data(doc_id)

@app.post("/feedback")
def store_feedback(fb: Feedback):
    print(fb)
    text = f"Question: {fb.question}\nApproved SQL: {fb.approved_sql}"
    embed_and_store_feedback(text)
    return {"status": "stored", "summary": text}


#TODO: UPDATE HOST 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 4000)))