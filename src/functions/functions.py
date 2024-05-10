import requests
import os
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("RAPID_KEY")
url = os.getenv("BASE_URL")
host = os.getenv("RAPID_HOST")

querystring = {"limit":"2"}

headers = {
	"X-RapidAPI-Key": api_key,
	"X-RapidAPI-Host": host
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())