from langchain.prompts import PromptTemplate

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


plotting_prompt = PromptTemplate.from_template("""
Draw the plot requested in the below query. Save the plot compulsorily as plot.png file. Do not save it anywhere else.

Query: 
{input}

Answer:
""")
