import chromadb
from chromadb.utils import embedding_functions
from typing import Optional
import os
import uuid
import json
from pathlib import Path

FEEDBACK_FILE = Path("feedback_store.json")

chromaHost = os.getenv('CHROMA_HOST', 'chromadb')
chromaPort = int(os.getenv("CHROMA_PORT", 8000))
client = chromadb.HttpClient(host=chromaHost, port=chromaPort) 
collection = client.get_or_create_collection(name="documents")

column_metadata = {
    "users": {
      "id": "Unique ID for each user (Primary key, Auto-incremented)",
      "username": "The user's display name (Regular column)",
      "email": "The user's email address (Regular column)",
      "password": "The user's encrypted password (Regular column)",
      "created_at": "Timestamp when the user was created (Default value is NOW())"
    },
    "products": {
      "id": "Unique ID for each product (Primary key, Auto-incremented)",
      "name": "Name of the product (Regular column)",
      "description": "Detailed information about the product (Regular column)",
      "price": "Selling price of the product (Regular column)",
      "stock": "Number of items available (Regular column)"
    },
    "orders": {
      "id": "Unique ID for each order (Primary key, Auto-incremented)",
      "user_id": "ID of the user who placed the order (Foreign key referencing users(id))",
      "order_date": "Date the order was placed (Regular column)",
      "total": "Total price of the order (Regular column)",
      "status": "Current status of the order (Regular column)"
    },
    "order_items": {
      "id": "Unique ID for each order item (Primary key, Auto-incremented)",
      "order_id": "ID of the related order (Foreign key referencing orders(id))",
      "product_id": "ID of the product in the order (Foreign key referencing products(id))",
      "quantity": "Number of units ordered (Regular column)",
      "price": "Price of the product at the time of order (Regular column)"
    },
    "categories": {
      "id": "Unique ID for each category (Primary key, Auto-incremented)",
      "name": "Name of the category (Regular column)",
      "description": "Details about the category (Regular column)"
    },
    "product_categories": {
      "id": "Unique ID for each mapping between product and category (Primary key, Auto-incremented)",
      "product_id": "ID of the product (Foreign key referencing products(id))",
      "category_id": "ID of the category (Foreign key referencing categories(id))"
    }
}



def embed_and_store(texts):
    collection.add(documents=texts, ids=[str(i) for i in range(len(texts))])

def retrieve_context(query):
    return collection.query(query_texts=[query], n_results=3)["documents"][0]

def fetch_chroma_data(doc_id: Optional[str] = None):
    try:
        if doc_id:
            result = collection.get(ids=[doc_id], include=["documents", "metadatas", "embeddings"])
            print("Document IDs:", result["ids"])
            print("\n")
            print("Documents:", result["documents"])
            print("\n")
            print("Metadata:", result["metadatas"])
            print("\n")
        else:
            result = collection.get(include=["documents", "metadatas", "embeddings"])
            print("Document IDs:", result["ids"], "\n")
            print("Documents:", result["documents"],"\n")
            print("Metadata:", result["metadatas"], "\n")

        return {"sucess":True}
    except Exception as e:
        return {"error": str(e)}

def load_schema_and_samples(conn, max_rows_per_table=3):
    schema_texts = []
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    #get all table names
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        print(f"Table Name {table_name}")
        queryForTable = f"DESCRIBE {table_name}"
        print(f"Executing Query For Table {queryForTable}")
        cursor.execute(queryForTable)
        columns = cursor.fetchall()
        # Use custom descriptions if available
        col_defs = []
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            description = column_metadata.get(table_name, {}).get(col_name, "No description available")
            col_defs.append(f"{col_name} ({col_type}) - {description}")
            print(f"\n{col_name} ({col_type}) - {description}")
        schema_text = f"Table: {table_name}\nColumns:\n" + "\n".join(col_defs)
        queryForTableData = f"SELECT * FROM {table_name} LIMIT {max_rows_per_table}"
        cursor.execute(queryForTableData)
        print(f"Executing Query For Table Data {queryForTableData}")
        rows = cursor.fetchall()
        sample_text = "\nSample rows:\n" + "\n".join(str(row) for row in rows)
        full_text = schema_text + sample_text
        schema_texts.append(full_text)

    embed_and_store(schema_texts)


def embed_and_store_feedback(text):
    # Store in ChromaDB
    doc_id = str(uuid.uuid4())
    collection = client.get_or_create_collection(name="documents")
    collection.add(documents=[text], ids=[doc_id])

    # Also store in local file
    with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        json.dump({"id": doc_id, "text": text}, f)
        f.write("\n")
        
def load_feedback_into_rag():
    if not FEEDBACK_FILE.exists():
        return

    with FEEDBACK_FILE.open("r", encoding="utf-8") as f:
        docs = [json.loads(line.strip()) for line in f if line.strip()]

    if docs:
        collection = client.get_or_create_collection(name="documents")
        collection.add(
            documents=[doc["text"] for doc in docs],
            ids=[doc["id"] for doc in docs]
        )