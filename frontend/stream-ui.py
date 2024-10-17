import streamlit as st
import requests
import pandas as pd

from PIL import Image
from io import BytesIO

# Function to send questions to the backend
def ask_backend(question):
    response = requests.post('http://127.0.0.1:8000/answer/', json={'query': question})
    return response

# Upload documents to the backend
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
page = st.sidebar.selectbox("Select a page:", ["Chat with AI", "Upload Document"])

# Initialize session state for storing chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page for chatting with AI (Ask a Question)
if page == "Chat with AI":
    st.title("Chat with AI")

    # Display chat history in the sidebar
    st.sidebar.subheader("Chat History")
    for i, (question, answer) in enumerate(st.session_state['chat_history']):
        st.sidebar.write(f"Q{i+1}: {question}")
        st.sidebar.write(f"A{i+1}: {answer}")
        st.sidebar.write("---")

    # Input for new question
    question = st.text_input("Type your question:")

    if st.button("Send"):
        if question:
            response = ask_backend(question)
            content_type=response.headers.get('Content-Type')
            answer=None
            if 'image' in content_type:  # Check if the content type is image
                try:
                    # Convert the response content to an image using PIL
                    img = Image.open(BytesIO(response.content))
                    answer='plot.png'
                    # Display the image in Streamlit
                    st.image(img, caption="Fetched Image from FastAPI", use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
        # Handle JSON responses
            elif 'application/json' in content_type:
                try:
                    json_data = response.json()
                except Exception as e:
                    st.error(f"Error parsing JSON: {e}")
                answer = json_data.get('answer', "No answer received")

            # Store the question and answer in session state
            st.session_state['chat_history'].append((question, answer))

            # Display the new question and answer
            st.write(f"**You:** {question}")
            st.write(f"**Answer:** {answer}")

            # Thumbs-up and thumbs-down buttons with NO space between
            feedback_html = """
            <div style="display: inline-block;">
                <button style="font-size: 30px; background-color: transparent; border: none; cursor: pointer;" onclick="window.location.href='#'">👍</button>
                <button style="font-size: 30px; background-color: transparent; border: none; cursor: pointer;" onclick="window.location.href='#'">👎</button>
            </div>
            """
            st.markdown(feedback_html, unsafe_allow_html=True)

            # Only display the graph if the response contains 'graph_data'
            if 'graph_data' in response:
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