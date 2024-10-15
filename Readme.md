There is a separate Backend for the LLM query retrieval and frontend for data insights manipulation and visualization.
The Demo video is attached with which you can get to know the working of the application.
We are tried the architecture to make it scalable and efficient.
To run the project
first clone the project , install all requirement from requirements.txt(pip install -r requirements.txt)
and then use the following instructions:
For frontend:
cd frontend
streamlit run stream-ui.py

for backend :
1.) cd db 
docker compose up -d
python -m setup
2.) we have used Google AI studio and hence we need to set GOOGLE_API_KEY env variable in .env file example GOOGLE_API_KEY=1234
3.) python -m server.main
