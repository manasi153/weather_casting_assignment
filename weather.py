import requests
import json
import pymongo
import traceback
import os
import time
import argparse
from functions import fetch_data,query_data,store_data


ACTIONS = ["Fetch", "Query"]


class weatherCast(object):
    def on_post(self, req, resp):
        try:
            parser = argparse.ArgumentParser(description="Fetch, Store and display weather data from OpenWeatherMap API")
            parser.add_argument("--city", help="City name for fetch or query")
            
            args = parser.parse_args()
    

            if ACTIONS in "Fetch":
                if not args.city:
                    print("Please provide a city name for fetching.")
                    return
                weather_data = fetch_data(args.city)
                store_data(weather_data)
                print(f"Weather data for {args.city} fetched and stored in MongoDB.")
            elif ACTIONS in "Query":
                if not args.city:
                    print("Please provide a city name for querying.")
                    return
                query_data(args.city)
            else:
                print("Invalid action. Use 'Fetch' or 'Query'.")         
                
        except Exception as e:
            traceback.print_exc()
            
            