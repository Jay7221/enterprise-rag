import streamlit as st
import requests
import pandas as pd
import json

def ask_backend(question):
    response = requests.post('http://127.0.0.1:8000/answer/', json={'query': question})
    return response.json()

def upload_document(uploaded_file, metadata):

    files = {'file': uploaded_file}
    response = requests.post(
        'http://127.0.0.1:8000/upload/',
        files=files,
        data=metadata
    )
    return response.json()

# Sidebar for page selection
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Ask a Question", "Upload Document"])

# Page for asking questions
if page == "Ask a Question":
    st.title("Ask Your Question")
    question = st.text_input("Type your question:")
    response = None


    if question:
        response = ask_backend(question)
        st.write(response['answer'])

    if response and 'graph_data' in response:
        df = pd.DataFrame(response['graph_data'])
        st.line_chart(df)

# Page for uploading documents
elif page == "Upload Document":
    st.title("Upload Document")

    # Input fields for document upload
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv"])

    if uploaded_file:
        metadata = st.text_input("Enter metadata for the file:")
        department = st.selectbox("Select Department", ["HR", "Finance", "IT", "Sales", "Marketing"])
        category = st.selectbox("Select Category", ["Reports", "Invoices", "Documents", "Others"])

        if st.button("Upload"):
            upload_response = upload_document(uploaded_file, {'metadata': metadata, 'department': department, 'category': category})
            st.write(upload_response['status'])
