from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel
from rag import fetch_chroma_data, retrieve_context, load_schema_and_samples
from mysql_db_utils import get_connection
import ollama
import uvicorn
import os


conn = get_connection()

load_schema_and_samples(conn)

app = FastAPI()

class Questions(BaseModel):
    question: str

@app.post("/query")
def answer_query(q: Questions):
    context = retrieve_context(q.question)
    prompt = f"""
You are an expert MySQL developer. Given the following database context and a natural language question,
generate a safe, syntactically correct, and precise MySQL query. Use only the tables and columns that are relevant.
Never delete or modify data. Only generate SELECT queries.

Context:\n{context}
Question:\n{q.question}
Write only the MySQL query no need to add any extra word or quote before and after query:
"""
    ollama_client = ollama.Client(host='http://localhost:11434')  # if accessing from host
    # response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])
    response = ollama_client.chat(model='mistral-small:latest', messages=[{"role": "user", "content": prompt}])
    #return response
    sql_query = response['message']['content'].strip()
    trimmed_sql_query = sql_query.replace('\n', ' ')
    print(trimmed_sql_query)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(trimmed_sql_query)
    result = cursor.fetchall()
    print(result)
    unique_rows = list(set(row for row in result))
    return {"query": trimmed_sql_query, "result": unique_rows}


@app.get("/fetch")
def fetch(doc_id: Optional[str] = Query(None, description="Document ID to fetch")):
    return fetch_chroma_data(doc_id)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)))