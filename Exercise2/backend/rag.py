import chromadb
from chromadb.utils import embedding_functions
from typing import Optional

client = chromadb.HttpClient(host='chromadb', port=8001)  # Not Local API
collection = client.get_or_create_collection(name="documents")

column_metadata = {
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
