import requests
import pymongo
import time
import os
from dotenv import load_dotenv

api_key = os.environ.get('YOUR_API_KEY')
db_name = os.environ.get('weather_data')
col_name = os.environ.get('Weather')

client = pymongo.MongoClient("mongodb://localhost:27017/") 
db = client.weather_data     
            
def fetch_data(city):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    data = response.json()
    if (response.status_code==200):
        return data
    else:
        return {}

def store_data(data):
    temp_k = data['main']['temp']
    temp_celsius = int(temp_k - 273.15)
    temp_fahrenheit = int((temp_celsius * 9/5) + 32)
    data["temp_celsius"] = temp_celsius
    data["temp_fahrenheit"] = temp_fahrenheit
    data["timestamp"] = time.time()
    db["Weather"].insert_one(data)

def query_data(city):
    result = db["Weather"].find_one({"name":city})
    if result:
        print(f"Weather data for {city}:")
        print(result)
    elif not result:
        print(f"Invalid {city}")
    else:
        print(f"No data found for the {city}")
 