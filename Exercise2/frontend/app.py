import streamlit as st
import requests

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

#TODO: env var
if st.button("Summon the Query"):
    res = requests.post("http://localhost:8000/query", json={"question": question})
    st.code(res.json()["query"])
    st.json(res.json()["result"])
