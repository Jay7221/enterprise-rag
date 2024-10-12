from .query_classification import query_classification_chain
from .table_query import csv_agent
from .rag_chain import rag_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda

def route(info):
    if info['query_type'] == 'Data Retrieval':
        return rag_chain
    elif info['query_type'] == 'Data Computation':
        return csv_agent

def parse_output(info):
    if isinstance(info,str):
        return info
    if 'answer' in info.keys():
        return info['answer']
    if 'output' in info.keys():
        return info['output']
    return "Query Failed"

qa_chain = (
    {"query_type": query_classification_chain, 'input': lambda x: x['query']}
    | RunnableLambda(route)
    | parse_output
)

if __name__ == "__main__":
    print(qa_chain.invoke({"query": "What is average sales ?"}))
    print(qa_chain.invoke({"query": "What is this book about "}))
