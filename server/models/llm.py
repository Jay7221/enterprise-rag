from langchain_google_genai import GoogleGenerativeAI
from server.configs.settings import LLM_MODEL

llm = GoogleGenerativeAI(model=LLM_MODEL)
