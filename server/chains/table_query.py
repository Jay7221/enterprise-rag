from server.models.csv_agent import csv_agent
import server.configs.settings


if __name__ == "__main__":
    print(csv_agent.invoke("What is the average sales ?"))
