import os
import streamlit as st
import mysql.connector
import pandas as pd
import math


DB_CONFIG = {
    'host': os.getenv("MYSQL_HOST", "host.docker.internal"),
    'port': int(os.getenv("MYSQL_PORT", 3306)),
    'user': os.getenv("MYSQL_USER", "root"),
    'password': os.getenv("MYSQL_PASSWORD", "root"),
    'database': os.getenv("MYSQL_DATABASE", "mydb")
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_table_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def get_table_data(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM `{table_name}`", conn)
    conn.close()
    return df

st.title("MySQL Table Viewer")

st.markdown("""
    <style>
        .stMainBlockContainer {
            max-width: 95% !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

tables = get_table_names()
clicked_table = None

# Set to 6 columns per row
max_cols = 6
num_rows = math.ceil(len(tables) / max_cols)

for row in range(num_rows):
    cols = st.columns(max_cols)
    for i in range(max_cols):
        idx = row * max_cols + i
        if idx < len(tables):
            with cols[i]:
                if st.button(tables[idx]):
                    clicked_table = tables[idx]

# Show table data
if clicked_table:
    st.subheader(f"Data from {clicked_table}")
    df = get_table_data(clicked_table)
    st.dataframe(df)