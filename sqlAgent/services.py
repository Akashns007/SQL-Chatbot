from bot import llm_process

async def process_query(question: str):
    """
    Process a user query through CrewAI's SQL agent.
    """
    try:
        async for chunk in llm_process(question):
            yield chunk
    except Exception as e:
        yield f"Error processing query: {str(e)}"


if __name__ == "__main__":
    question = "show employee with highest salary?"
    process_query(question)