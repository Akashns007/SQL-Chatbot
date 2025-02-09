from langchain_community.utilities import SQLDatabase  
from langchain.chains import create_sql_query_chain
from langchain_community.chat_models import ChatOpenAI, ChatOllama
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from dotenv import load_dotenv
from crewai_tools import RagTool
import warnings

warnings.filterwarnings("ignore")
load_dotenv()

# Initialize LLM
llm = ChatOllama(
    model="mistral:latest",
    base_url="http://localhost:11434"
)

# llm = ChatOpenAI(
#     model="ollama/mistral",
#     base_url="http://localhost:11434"
# )

# Connect to SQLite Database
db = SQLDatabase.from_uri("sqlite:///sqlite_large.db")

# Create the Query Execution Tool
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

# CrewAI Tool Wrapping for SQL Queries
class SQLQueryTool(RagTool):
    name: str = "SQL Query Tool"
    description: str = "Executes SQL queries on an SQLite database and returns results."

    def _run(self, question: str) -> str:
        """
        Generates and executes an SQL query based on a natural language question.
        """
        try:
            # Generate SQL query
            sql_query = write_query.invoke({"question": question})
            print(f"Generated Query: {sql_query}")  # Debugging Output

            # Check if the generated query references an existing table
            available_tables = db.get_usable_table_names()
            if not any(table in sql_query for table in available_tables):
                return f"Error: The query references a table that doesn't exist. Available tables: {available_tables}"

            # Execute Query
            result = execute_query.invoke({"query": sql_query})
            
            dialect = db.dialect  
            tables = db.get_table_names()  
            context = db.get_context()  # If this is a method, call it properly  
            
            
            print(result)
            
            return (
                f"Database Dialect: {dialect}\n"
                f"Tables Available: {', '.join(tables) if tables else 'No tables found'}\n"
                f"Database Context: {context}\n"
                f"User Question: {question}\n"
                f"Result: {result}"
            )

        except Exception as e:
            return f"Error executing query: {str(e)}"

if __name__ == "__main__":
    sql_tool = SQLQueryTool()
    response = sql_tool.run("which department has the highest salary?")
    print(response)
