import requests
import json
import csv
import os
import time
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

# Function to fetch aircraft data and save to CSV
def fetch_and_save_aircraft_data(csv_file_path):
    # Replace with the actual latitude, longitude, and radius values
    latitude = 57.2037  # London Heathrow Airport latitude
    longitude = 2.2002  # London Heathrow Airport longitude
    radius = 200  # 200-mile radius

    # Replace with the actual API endpoint you want to use
    api_url = f'http://api.airplanes.live/v2/point/{latitude}/{longitude}/{radius}'

    # Make the GET request
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        aircraft_data = response.json()

        # Create a list of dictionaries for each aircraft
        aircraft_list = []
        for aircraft in aircraft_data['ac']:
            altitude = aircraft.get('alt_baro', None)
            flight = aircraft.get('flight', None)
            mag_heading = aircraft.get('mag_heading', None)

            aircraft_entry = {
                "hex": aircraft['hex'],
                "flight": flight,
                "ownOp": aircraft.get('ownOp', None),
                "desc": aircraft.get('desc', None),
                "altitude": altitude,
                "lon": aircraft['lon'],
                "lat": aircraft['lat'],
                "mag_heading": mag_heading
            }
            aircraft_list.append(aircraft_entry)

        # Write the data to a CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            # Define CSV header
            fieldnames = ["hex", "flight", "ownOp", "desc", "altitude", "lon", "lat", "mag_heading"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write aircraft data
            writer.writerows(aircraft_list)

        print(f"Aircraft data saved successfully to: {csv_file_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Function to update hosted feature layer
def update_feature_layer(csv_file_path, item_id, username, password):
    # Connect to ArcGIS Online
    gis = GIS('https://www.arcgis.com', username, password)

    # Get the hosted feature layer
    item = gis.content.get(item_id)
    feature_layer_collection = FeatureLayerCollection.fromitem(item)

    # Overwrite the feature layer with the local CSV file
    feature_layer_collection.manager.overwrite(csv_file_path)

    print(f"Feature layer updated successfully")

# Path to save the CSV file
csv_file_path = r'C:\Users\DELL\OneDrive\Desktop\WEBGIS2\aircraft_data.csv'

# Replace with the actual item ID of your hosted feature layer
item_id = "da43d8ed3e614595ad8f68e748155752"

# Replace with your ArcGIS Online username and password
username = "a.hani.22_abdn"
password = "0A112b358c"

# Main loop to repeat the process every 30 seconds
while True:
    fetch_and_save_aircraft_data(csv_file_path)
    update_feature_layer(csv_file_path, item_id, username, password)
    time.sleep(30)  # Sleep for 30 seconds before the next iteration
