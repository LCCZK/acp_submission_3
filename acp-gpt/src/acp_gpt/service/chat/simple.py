import json
import logging
from acp_gpt.service.llm_client import call_llm


logger = logging.getLogger("uvicorn")


def run_simple_chat(prompt: str) -> dict:
    tools =[]
    steps = []
    messages: list = [{"role": "user", "content": prompt}]
    

    response = call_llm(messages, tools)
    msg = response.choices[0].message

    return {"response": msg.content,
            "steps": steps,}