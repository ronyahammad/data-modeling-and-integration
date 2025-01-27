import requests
import json
import csv

class WaterQualityAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, data_type):
        url = f"{self.base_url}/{data_type}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()  
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {data_type}: {e}")
            return None

    def save_to_csv(self, data, filename):
        if data:
            
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader() 
                writer.writerows(data)  
            print(f"Data saved to {filename}")
        else:
            print("No data to save.")


def fetch_and_save_data():
    api = WaterQualityAPI("http://localhost:8081")


    data_types = ['sensors', 'reports', 'temperature', 'ph', 'turbidity']


    for data_type in data_types:
        print(f"Fetching data for {data_type}...")
        data = api.get_data(data_type)

        if data:

            api.save_to_csv(data, f"{data_type}.csv")
        else:
            print(f"No data found for {data_type}")



if __name__ == "__main__":
    fetch_and_save_data()
