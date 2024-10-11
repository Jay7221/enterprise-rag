from .chain_utils import format_documents
from server.db.db_utils import retriever
from server.models.llm import llm
from langchain_core.runnables import RunnableLambda

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from .prompts import query_prompt

def add_context(info):
    info['context'] = format_documents(retriever.invoke(info['query']))
    return info

simple_rag_chain = (
    RunnableLambda(add_context)
    | query_prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    print(simple_rag_chain.invoke({"query": "What is the book about ?"}))
