from server.db.db_utils import retriever, get_department_list
from server.models.llm import llm


from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from .prompts import query_prompt, department_prompt

def format_documents(docs):
    """Format a list of document objects into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def format_department_data(departments):
    """Format department data for display."""
    return "\n".join([f"- {dept['name']}: {dept['description']}" for dept in departments])

def fetch_query_type_descriptions(query):
    """Return descriptions of each query type for classification."""
    return '\n'.join([f"{query_type}: {description}" for (query_type, description) in QUERY_TYPES.items()])

def get_csv_file_names_and_descriptions(data):
    """Format CSV file information for display."""
    return "\n".join([f"{file_data['name']}:{file_data['description']}" for file_data in data])

# Chains for different functionalities
rag_chain = (
    {"context": retriever | format_documents, "query": RunnablePassthrough()}
    | query_prompt
    | llm
    | StrOutputParser()
)

department_chain = (
    {"departments": get_department_list, "query": RunnablePassthrough()}
    | department_prompt
    | llm
    | StrOutputParser()
)

