from collections import deque
from datetime import datetime
import os
import time
import requests
import json

import pickle
from pathlib import Path

import traceback

import pandas as pd



def append_game_to_csv(file_name, game_data):
    file_path = Path(file_name)
    
    # Convert the game data to a DataFrame
    df_new = pd.DataFrame([game_data])
    
    if file_path.exists():
        # Load existing data
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    
    # Save the updated DataFrame to an Excel file
    df_combined.to_csv(file_path, index=False)





def print_log(*args):
    print(f"[{str(datetime.now())[:-3]}] ", end="")
    print(*args)

def get_all_app_id():
    apps_ids = []
   
    # Read the app ids from the file
    with open('app_ids_with_reviews.txt', 'r') as f:
        all_app_ids = f.readlines()
        all_app_ids = [appid.strip() for appid in all_app_ids]
        all_app_ids = list(map(int, all_app_ids))
    return all_app_ids



def main():
    print_log("Started Steam scraper process", os.getpid())

    # get the app name, description and append to 
    #file_name = "games.xlsx"
    file_name = "games.csv"

    all_app_ids = get_all_app_id()

    print_log('Total number of apps on steam:', len(all_app_ids))


    for appid in all_app_ids:
        try:
            response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=turkish")
            if response.status_code == 200:
                appdetails = response.json().get(str(appid), {})
                if not appdetails.get("success", False):
                    continue
                
                data = appdetails.get("data", {})
                game_data = {
                    "ID": str(data.get("steam_appid", "")),
                    "Name": str(data.get("name", "")),
                    "Type": str(data.get("type", "")),
                    "Detailed Description": str(data.get("detailed_description", "")),
                    "Price": str(data.get("price_overview", {}).get("final_formatted", "N/A")),
                    "Release Date": str(data.get("release_date", {}).get("date", "N/A")),
                    "Platforms": ", ".join([str(k) for k, v in data.get("platforms", {}).items() if v]),
                    "Developers": ", ".join([str(dev) for dev in data.get("developers", [])]),
                    "Genres": ", ".join([str(genre.get("description", "N/A")) for genre in data.get("genres", [])]),
                    "Categories": ", ".join([str(category.get("description", "N/A")) for category in data.get("categories", [])]),
                    "Game Modes": ", ".join([str(mode.get("description", "N/A")) for mode in data.get("categories", [])]),
                    "Features": ", ".join([str(feature.get("description", "N/A")) for feature in data.get("features", [])]),
                    "System Requirements (Min.)": str(data.get("pc_requirements", {}).get("minimum", "N/A")),
                    "System Requirements (Rec.)": str(data.get("pc_requirements", {}).get("recommended", "N/A")),
                    "Age Rating": str(data.get("required_age", "N/A")),
                    "Links": ", ".join([str(link) for link in data.get("support_info", {}).values()]),
                }

                
                append_game_to_csv(file_name, game_data)
                print(f"Saved: {game_data['Name']}")
        except Exception as e:
            print(f"Error processing app {appid}: {e}")

    
    print_log('Successful run. Program Terminates.')

if __name__ == '__main__':
    main()