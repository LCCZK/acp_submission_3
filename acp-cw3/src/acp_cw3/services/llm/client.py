from openai import OpenAI
from acp_cw3.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

def call_llm(messages: list, tools: list):
    return client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
