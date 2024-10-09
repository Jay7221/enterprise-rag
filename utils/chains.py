from db_utils import retriever

from langchain_core.runnables import RunnablePassthrough

from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

llm = GoogleGenerativeAI(model="gemini-pro")

query_prompt = PromptTemplate.from_template("""
Answer the below query on the basis of context provided.

Query: 
{query}

Context:
{context}

Answer:
""")

rag_chain = (
    {"context": retriever | format_docs, "query": RunnablePassthrough()}
    | query_prompt
    | llm
)



if __name__ == "__main__":
    print(rag_chain.invoke("What is the name of the book ?"))
    print(rag_chain.invoke("What is the book about ?"))
