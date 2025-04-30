import streamlit as st
import requests
import pandas as pd
import os
import mysql.connector
import logging

DB_CONFIG = {
    'host': os.getenv("MYSQL_HOST", "host.docker.internal"),
    'port': int(os.getenv("MYSQL_PORT", 3306)),
    'user': os.getenv("MYSQL_USER", "root"),
    'password': os.getenv("MYSQL_PASSWORD", "root"),
    'database': os.getenv("MYSQL_DATABASE", "mydb")
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_table_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

apiHost = os.getenv('API_HOST', 'backend')
apiPort = int(os.getenv("API_PORT", 4000))

st.title("From Blah Blah to SELECT App ")
st.markdown("""
    <style>
        .stMainBlockContainer {
            max-width: 95% !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)
question = st.text_input("Ask away, but no refunds on bad answers!")



# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Initialize session state
if "query" not in st.session_state:
    st.session_state["query"] = None
if "approved" not in st.session_state:
    st.session_state["approved"] = False

if st.button("Summon the Query"):
    logging.info("Summon button clicked.")
    try:
        res = requests.post(f"http://{apiHost}:{apiPort}/query", json={"question": question})
        res.raise_for_status()
        st.session_state["query"] = res.json()["query"]
        st.session_state["approved"] = False  # reset approval if new query
        logging.info(f"Query received and stored: {st.session_state['query']}")
    except Exception as e:
        logging.error(f"Failed to fetch query: {e}")
        st.error("Failed to generate SQL query.")

# Always show the query if available
if st.session_state["query"]:
    st.code(st.session_state["query"])
    if st.session_state["approved"] == False:
        if st.button("👍 Approve this SQL"):
            logging.info("Approve button clicked.")
            try:
                res = requests.post(f"http://{apiHost}:{apiPort}/feedback", json={
                    "question": question,
                    "approved_sql": st.session_state["query"]
                })
                res.raise_for_status()
                st.success("Thank you! Feedback saved.")
                st.session_state["approved"] = True
                logging.info("Feedback successfully sent.")
            except Exception as e:
                logging.error(f"Failed to send feedback: {e}")
                st.error("Failed to save feedback.")

    try:
        df = get_table_data(st.session_state["query"])
        st.dataframe(df)
        logging.info("Table data successfully loaded and displayed.")
    except Exception as e:
        logging.error(f"Failed to load table data: {e}")
        st.error("Failed to load table data.")  