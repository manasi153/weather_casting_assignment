import requests
import json
import pymongo
import traceback
import os
import time
import argparse
from functions import fetch_data,query_data,store_data


ACTIONS = ["Fetch", "Query"]

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
    temp_k = data['weather_data']['temp']
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
 

class weatherCast(object):
    def on_post():
        try:
            parser = argparse.ArgumentParser(description="Fetch, Store and display weather data from OpenWeatherMap API")
            parser.add_argument("--city", help="City name for fetch or query")
            
            args = parser.parse_args()
    

            if "Fetch" in ACTIONS:
                if not args.city:
                    print("Please provide a city name for fetching.")
                    return
                weather_data = fetch_data(args.city)
                store_data(weather_data)
                print(f"Weather data for {args.city} fetched and stored in MongoDB.")
            elif "Query" in ACTIONS:
                if not args.city:
                    print("Please provide a city name for querying.")
                    return
                query_data(args.city)
            else:
                print("Invalid action. Use 'Fetch' or 'Query'.")         
                
        except Exception as e:
            traceback.print_exc()
            
    if __name__ == "__main__":
        on_post()            