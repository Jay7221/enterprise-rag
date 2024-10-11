from .query_classification import query_classification_chain
from .table_query import csv_agent
from .simple_rag import simple_rag_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda

def route(info):
    if info['query_type'] == 'Data Retrieval':
        return simple_rag_chain
    elif info['query_type'] == 'Data Computation':
        return csv_agent

def parse_output(info):
    if type(info) == str:
        return info
    return info['output']

qa_chain = (
    {"query_type": query_classification_chain, "query": lambda x: x['query'], 'input': lambda x: x['query']}
    | RunnableLambda(route)
    | parse_output
)

if __name__ == "__main__":
    print(qa_chain.invoke({"query": "What is average sales ?"}))
    print(qa_chain.invoke({"query": "What is this book about "}))
