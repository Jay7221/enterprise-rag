# Enterprise RAG System

Welcome to our Enterprise RAG (Retrieval-Augmented Generation) System project repository. This system enables enterprises to extract insights from their data using Language Model (LLM) queries.

## Project Structure

### Directories

- **db/**: Contains Docker configuration (`docker-compose.yml`), setup scripts (`reset.py`, `setup.py`), and potentially database-related utilities.
- **files/**: Holds sample data files such as `sample.csv`.
- **frontend/**: Includes a Streamlit-based UI (`stream-ui.py`) for data manipulation and visualization.
- **notebooks/**: Jupyter notebooks for exploring RAG functionalities (`rag.ipynb`, `table_rag.ipynb`).
- **server/**: Backend logic for LLM query retrieval and data processing.
  - **chains/**: Modules for different RAG chains (`chain_utils.py`, `qa.py`, `simple_rag.py`, etc.).
  - **configs/**: Configuration settings (`settings.py`).
  - **db/**: Database utilities (`db_utils.py`).
  - **models/**: Models used for data processing (`csv_agent.py`, `embeddings.py`, `llm.py`).
  - **services/**: Services for document processing (`document_processing.py`).

### Instructions to Run

To run the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jay7221/enterprise-rag
   cd enterprise-rag
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setting up the frontend:**
   ```bash
   cd frontend
   streamlit run stream-ui.py
   ```

4. **Setting up the backend:**

   a. Start the database:
   ```bash
   cd ../db
   docker-compose up -d
   python -m setup
   ```

   b. Set up necessary environment variables (e.g., Google API key):
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

   c. Start the backend server:
   ```bash
   cd ../server
   python -m server.main
   ```

### Additional Notes

- **Scalability and Efficiency:** The architecture is designed to be scalable and efficient, utilizing Streamlit for frontend interactivity and Docker for backend service isolation.
- **Demo Video:** For a demonstration of the application, please refer to the attached demo video.
