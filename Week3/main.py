import logging
import time

from langchain_ollama import OllamaLLM            # ✅ new package
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.tools import Tool                  # ✅ preferred import
from langchain_community.agent_toolkits.sql.base import create_sql_agent, SQLDatabaseToolkit
from langchain.agents import AgentType


# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("sql_queries.log", mode="w")
    ]
)
logger = logging.getLogger(__name__)


def safe_invoke(query: str, db_chain: SQLDatabaseChain) -> str:
    """
    Clean up SQL queries and call db_chain.invoke() with the correct input schema.
    Logs execution time and cleaned query.
    """
    cleaned_query = (
        query.replace('`"', '"')
             .replace('"`', '"')
             .replace('"', '')  # SQLite is fine with bare identifiers
    )

    logger.info(f"[SQL] Cleaned Query: {cleaned_query}")

    start_time = time.time()
    # ✅ Modern SQLDatabaseChain expects {"query": ...}
    result = db_chain.invoke({"query": cleaned_query})
    elapsed = (time.time() - start_time) * 1000
    logger.info(f"[SQL] Query executed successfully in {elapsed:.1f} ms")

    # Most builds return a dict with "result"; if yours returns a string, fall back.
    return result["result"] if isinstance(result, dict) and "result" in result else str(result)


def main():
    logger.info("Connecting to SQLite database...")
    db = SQLDatabase.from_uri("sqlite:///sample.db")

    logger.info("Initializing Ollama with llama3...")
    llm = OllamaLLM(model="llama3")              # ✅ updated class

    logger.info("Setting up SQLDatabaseChain (verbose mode ON)...")
    db_chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        verbose=True,
    )

    logger.info("Wrapping db_chain with safe_invoke...")
    # Make sure the tool only accepts a single string arg (what agents expect)
    sql_tool = Tool(
        name="SQLDatabaseTool",
        func=db_chain.invoke,  # ✅ pass natural language through
        description=(
            "Answer questions about the SQLite database. "
            "Input should be a natural-language question, not raw SQL."
        ),
    )

    logger.info("Building SQL toolkit...")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    logger.info("Creating SQL agent...")
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,                      # ✅ pass toolkit, not a list
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    logger.info("✅ Agent is ready. Entering interactive loop.")
    while True:
        query = input("\nAsk me something (or type 'exit'): ")
        if query.lower() == "exit":
            logger.info("Exiting program. Goodbye!")
            break
        logger.info(f"User Query: {query}")
        try:
            # Avoid deprecated .run(); pass the right input shape.
            response = agent.invoke({"input": query})      # ✅ correct call
            print("\n🤖 Agent:", response["output"])
        except Exception as e:
            logger.error(f"❌ Error while processing query: {e}")

if __name__ == "__main__":
    main()
