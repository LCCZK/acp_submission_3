# main.py
import json
from openai import OpenAI
from tools.employee_look_up import db_lookup, SCHEMA as db_schema
from tools.weather import get_weather, SCHEMA as weather_schema
import time

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

TOOL_FUNCTIONS = {
    "db_lookup": db_lookup,
    "get_weather": get_weather,
}

TOOLS:list = [db_schema, weather_schema]

def run(prompt: str):
    messages:list = [{"role": "user", "content": prompt}]

    while True:
        response = client.chat.completions.create(
            model="local-model",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        if not message.tool_calls:
            print ("====================================")
            print("FINAL RESPOND:")
            print ("====================================")
            print(message.content)
            print ("====================================")
            return


        messages.append(message)

        for call in message.tool_calls:
            func_name = call.function.name
            args = json.loads(call.function.arguments)
            print(f"\nTOOL USAGE: Calling {func_name}({args})")

            try:
                result = TOOL_FUNCTIONS[func_name](**args)
                print(f"TOOL RETURN: {result}\n")
            except Exception as e:
                result = {"error": str(e)}
                print(f"TOOL FAILED: {e}")

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })


if __name__ == "__main__":
    run("Find all engineers or developers in the company, show all their names and emails. Tell me the current weather in Edinburgh. Find all people in engineering department, list their name and the id. Tell me the weather in Edinburgh. Find all engineers or developers in the company.")