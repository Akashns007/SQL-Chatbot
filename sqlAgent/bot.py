import warnings
from tools import SQLQueryTool
from dotenv import load_dotenv
import ollama
import asyncio

warnings.filterwarnings("ignore")
load_dotenv()

# Initialize SQL Query Tool
sql_tool = SQLQueryTool()

def process_with_ollama(model="mistral", query=""):
    """
    Processes the query with Ollama model and streams the response.
    """
    system_prompt = """
                    You are a Database Analyst. You will receive a user question
                    and the results from a database.
                    Your job is to only answer the question and not confuse the user.
                    **Never explain any query to the user.**
                    Return results in lists, make a list of each row and return.
                    if the result is very big then only give some of those results, but u must return the results to the user
                    **Never explain the meaning of the words in the result, only explain the result as a whole **
    """
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        stream=True,
    )

async def llm_process(question):
    """
    Runs the SQL query and streams the LLM response.
    """
    tool_output = sql_tool.run(question)
    query = f"User question: {question}\n{tool_output}"
    response_stream = process_with_ollama(query=query)

    # Wrap sync call in asyncio to avoid blocking
    for chunk in response_stream:
        await asyncio.sleep(0)  # Yield control to avoid blocking
        yield chunk["message"]["content"]

        
if __name__ == "__main__":
    question = "show employee with highest salary?"
    for chunk in llm_process(question):
        print(chunk["message"]["content"])
