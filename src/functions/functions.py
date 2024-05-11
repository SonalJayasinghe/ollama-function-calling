import requests
import os
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("RAPID_KEY")
url = os.getenv("BASE_URL")
host = os.getenv("RAPID_HOST")

def get_exercise_list():
    querystring = {"limit":"10"}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def get_exercise_by_bodypart(name: str):
    querystring = {"limit":"2"}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host
    }
    response = requests.get(url+(f"/bodyPart/{name}"), headers=headers, params=querystring)
    return response.json()
