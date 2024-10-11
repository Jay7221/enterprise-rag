from langchain_experimental.agents.agent_toolkits import create_csv_agent

from .llm import llm
from server.db.db_utils import get_csv_file_paths


csv_agent = create_csv_agent(llm, get_csv_file_paths(), verbose=True, allow_dangerous_code=True)
