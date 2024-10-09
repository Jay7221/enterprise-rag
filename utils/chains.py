from db_utils import retriever, get_departments
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Function to format document content
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Function to format department information
def format_departments(departments):
    formatted = "\n".join([f"- {dept['name']}: {dept['description']}" for dept in departments])
    return formatted

# Function to get formatted department information
def get_formatted_departments():
    return format_departments(get_departments())

# Function to classify query types
QUERY_TYPES = {
    "Data Retrieval": "Involves retrieving or lookup of simple facts or data. There should be little to no processing involved. Eg: What is the name of company providing fire service.",
    "Data Computation": "Involves numerical computation on some tables or numerical data to arrive on answer. Eg: Who are the top 5 most profitable customers based on sales from July to June.",
    "Decision Making": "Involves complex multi-step thought process to arrive at an answer. Eg: What are the expected problems to be faced while increasing EV production of Delhi unit by 10 percent in next 4 months.",
}

def get_query_types(query):
    return '\n'.join([f"{query_type}: {description}" for (query_type, description) in QUERY_TYPES.items()])

# Function to format CSV file names and descriptions
def format_csv_file_names(data):
    return "\n".join([f"{file_data['name']}:{file_data['description']}" for file_data in data])

# Function to get relevant CSV files
def get_csv_files(query):
    return [
        {"name": "Sales.csv", "description": "Data on sales of EV in Delhi."},
        {"name": "Operations.csv", "description": "Data on quality control operations in Gurgaon plant."},
    ]

def get_csv_file_descriptions(query):
    return format_csv_file_names(get_csv_files(query))

llm = GoogleGenerativeAI(model="gemini-pro")

# Define prompt templates
query_prompt = PromptTemplate.from_template("""
Answer the below query on the basis of context provided.

Query: 
{query}

Context:
{context}

Answer:
""")

department_prompt = PromptTemplate.from_template("""
You are an AI that identifies which department is most related to a given query. 
Based on the descriptions of departments, suggest the department that best matches the query.

Departments:
{departments}

Query:
{query}

Department:
""")

query_classification_prompt = PromptTemplate.from_template("""
Classify the below query into one of the query types. You need to return only the name of the query type, do not return anything else.

Query:
{query}

Query Types:
{query_types}
""")

document_selection_prompt = PromptTemplate.from_template("""
Given the below query and csv files with their description, find the list most relevant csv files that will be able to answer the query. Just return the list filenames in python list form [file1, file2, ..., file3] and nothing else. Even if there is a single file, return it in list form.

Query:
{query}

Files:
{file_descriptions}

Relevant Files: 
""")

# Chains for different functionalities
rag_chain = (
    {"context": retriever | format_docs, "query": RunnablePassthrough()}
    | query_prompt
    | llm
    | StrOutputParser()
)

department_chain = (
    {"departments": get_departments, "query": RunnablePassthrough()}
    | department_prompt
    | llm
    | StrOutputParser()
)

query_classification_chain = (
    {"query_types" : get_query_types ,"query": RunnablePassthrough()}
    | query_classification_prompt
    | llm
    | StrOutputParser()
)

document_selection_chain = (
    {"file_descriptions": get_csv_file_descriptions, "query": RunnablePassthrough()}
    | document_selection_prompt
    | llm
    | StrOutputParser()
)



if __name__ == "__main__":

    # Example invocations
    print(rag_chain.invoke("What is the name of the book ?"))
    print(rag_chain.invoke("What is the book about ?"))

    print(department_chain.invoke("How do I reset my Windows PC ?"))

    print(query_classification_chain.invoke("Which team handles zoom dashboard integrations ?"))
    print(query_classification_chain.invoke("Which are the top 5 customers by percentage of sales ?"))
    print(query_classification_chain.invoke("What is the process for hiring a candidate ?"))
    print(query_classification_chain.invoke("Is it worth it to invest in EV sales to reduce pressure on Delhi units ?"))

    print(document_selection_chain.invoke("What is the total failure rate for pipes section production line ?"))
    print(document_selection_chain.invoke("Which are the top 5 best selling EV models in Delhi."))
