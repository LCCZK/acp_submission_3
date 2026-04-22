import requests

def get_weather(city: str) -> dict:
    response = requests.get(
        f"https://wttr.in/{city}?format=j1",
        timeout=5
    )
    response.raise_for_status()
    data = response.json()

    current = data["current_condition"][0]
    return {
        "city": city,
        "temp_c": current["temp_C"],
        "feels_like_c": current["FeelsLikeC"],
        "condition": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"],
        "wind_kph": current["windspeedKmph"]
    }


# SCHEMA = {
#     "type": "function",
#     "function": {
#         "name": "get_weather",
#         "description": "Get the current weather for a city. Returns temperature, condition, humidity and wind speed.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "city": {
#                     "type": "string",
#                     "description": "The city name, e.g. 'London' or 'Edinburgh'"
#                 }
#             },
#             "required": ["city"]
#         }
#     }
# }

if __name__ == "__main__":
    print(get_weather("Edinburgh"))