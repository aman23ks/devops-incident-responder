from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.prompts.prompts import SYSTEM_PROMPT
from app.tools.tools import fetch_log_file, rag_retrieve, store_final_report
import os
from dotenv import load_dotenv

load_dotenv()
# Collect registered tools
tools = [fetch_log_file, rag_retrieve, store_final_report]

def run_agent(incident_json: str):
    """
    Run the ReAct agent on the given incident JSON string.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is absolutely required but missing. Go to Render settings and add it!")

    model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
    model = ChatOpenAI(model=model_name, temperature=0, api_key=api_key)
    
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    prefixed_input = (
        "These are the details regarding the incident. "
        "Investigate this issue step by step using the available tools "
        "and prepare a comprehensive incident report for the developer.\n\n"
        f"Incident details:\n{incident_json}"
    )

    return agent.invoke({"messages": [{"role": "user", "content": prefixed_input}]})