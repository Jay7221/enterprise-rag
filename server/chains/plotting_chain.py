from server.models.llm import llm
import server.configs.settings
from .prompts import plotting_prompt
from langchain_experimental.agents.agent_toolkits import create_csv_agent

from server.db.db_utils import get_csv_file_paths

def plot_with_agent(info):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    csv_agent = create_csv_agent(llm, get_csv_file_paths(), verbose=True, allow_dangerous_code=True)
    prompt = plotting_prompt.invoke(info)
    return csv_agent.invoke(prompt.text)

if __name__ == "__main__":
    print(plot_with_agent({"input": "Plot bar graph of sales v/s country"}))
