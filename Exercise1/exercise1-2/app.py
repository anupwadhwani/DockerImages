import streamlit as st
import os

# Target directory inside the container
TARGET_DIR = "uploads"
os.makedirs(TARGET_DIR, exist_ok=True)

st.title("Upload File to Container and View Content")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=None)

if uploaded_file is not None:
    # Save the file to the target directory
    save_path = os.path.join(TARGET_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved to: `{save_path}`")

    # Try to show contents (text-based files)
    try:
        file_contents = uploaded_file.read().decode("utf-8")
        st.subheader("File Contents")
        st.code(file_contents, language='text')
    except Exception as e:
        st.warning("Could not display file contents (non-text or binary file).")
        st.error(str(e))
