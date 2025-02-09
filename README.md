# SQL Chatbot Project  

This project is a full-stack SQL chatbot application built using React for the frontend and Python for the backend. The chatbot is powered by an LLM and allows users to query an SQL database using conversational language. 

## Project Structure  

```
/sql-chatbot  
├── chatbot-ui          # Frontend built using React  
├── sqlAgent            # Backend built using FastAPI  
│   ├── main.py         # FastAPI app entry point  
│   ├── services.py     # Core service for query handling  
│   ├── create_db.py    # Script for database creation  
│   └── db              # Contains SQLite databases  
├── requirements.txt    # Python dependencies  
└── .env                # Environment variables  
```  

---

## Prerequisites  

1. **Node.js (>= 14)**: For the React frontend  
2. **Python (>= 3.8)**: For the FastAPI backend  
3. **Ollama (AI Model Runner)**  
   Ollama is required to run AI models locally for chatbot responses. Install Ollama.  


   **Note:**  download Ollama from the [official website](https://ollama.com) and follow the installation instructions.  
   
4. **SQLite**: To manage local databases  
5. **FastAPI and Dependencies** (see `requirements.txt`)  

---

## Getting Started  

### Backend Setup  

1. Create and activate a virtual environment:  
   ```bash
   python -m venv venv  
   source venv/bin/activate   # macOS/Linux  
   .\venv\Scripts\activate    # Windows  
   ```  

2. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt  
   ```  

3. Set up the database by running:  
   ```bash
   python create_db.py  
   ```  

4. Start the FastAPI server:  
   ```bash
   python main.py  
   ```  
   The server will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).  

### Frontend Setup  

1. Navigate to the `chatbot-ui` directory:  
   ```bash
   cd chatbot-ui  
   ```  

2. Install the dependencies:  
   ```bash
   npm install  
   ```  

3. Start the React development server:  
   ```bash
   npm start  
   ```  
   The frontend will be available at [http://localhost:3000](http://localhost:3000).  

---

## Running the Full Application  

Ensure that both the backend and frontend servers are running simultaneously.  

---

## Usage Instructions  

- Open your browser and go to [http://localhost:3000](http://localhost:3000).  
- Enter your queries in natural language to interact with the SQL database through the chatbot interface.  

---

## Notes  

- **Ollama Models**: Ensure that Ollama is running and configured to provide AI responses for chatbot queries. Use:  
  ```bash
  ollama pull Mistral   #Different models can be used... requires changing configuration in backend.
  ```  
 
- For **Windows**: the Ollama application should be running, 
  ```bash
  ollama serve
  ``` 

- The chatbot currently relies on `sqlite_large.db` for queries. Ensure this database is populated.  

- Update the `.env` file if required for custom configurations.  

---

## Contributions  

Contributions are welcome! Please create a pull request or raise an issue on GitHub if you encounter any problems.

