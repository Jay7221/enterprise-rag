from server.models.llm import llm
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

QUERY_TYPES = {
    "Data Retrieval": '''Involves retrieving or lookup of facts or data from text documents. Eg: 
    What is the name of company providing fire service. 
    What is the process to modify company logo.
    ''',
    "Data Computation": '''Involves numerical computation on some tables or numerical data to arrive on answer. Eg: 
    Who are the top 5 most profitable customers based on sales from July to June.
    Which department has highest profit to sales ratio in Delhi.
    ''',
    "Data Plotting": '''Involves plotting of data. This usually involves drawing a line graph, bar graph or pie chart. Eg:
    Give me a pie chart of sales classified by shipped.
    Give me a bar graph of sales by product type.
    '''
}

def get_query_types():
    return '\n'.join([f"{query_type}: {description}" for (query_type, description) in QUERY_TYPES.items()])

query_classification_prompt = PromptTemplate.from_template("""
Classify the below query into one of the query types. You need to return only the name of the query type, do not return anything else.

Query:
{query}

Query Types:
{query_types}
""").partial(query_types=get_query_types())

query_classification_chain = (
    query_classification_prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    print(query_classification_chain.invoke({"query": "What is the average usage based on recent data??"}))
