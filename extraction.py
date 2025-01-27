import psycopg2
import mysql.connector
from cassandra.cluster import Cluster
import pandas as pd

from pymongo import MongoClient
import csv
import requests
import xml.etree.ElementTree as ET

BASEX_URL = "http://localhost:8984/rest"
DATABASE_NAME = "customer_service_management"
USERNAME = "admin"
PASSWORD = "admin" 

# PostgreSQL Data Extraction and CSV Writing


def fetch_postgres_data():
    conn_params = {
        "dbname": "admin",
        "user": "postgres",
        "password": "admin",
        "host": "localhost",
        "port": 5433
    }

    # Connect to PostgreSQL
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cursor:
            tables = ["AreaTypes", "CollectionFrequencies", "Clients_list", "WasteCategories", "CollectionSchedule",
                      "WasteDisposal", "BillingRecords", "BillingDetails"]

            for table in tables:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                # Write data to CSV
                with open(f"waste_postgres_{table.lower()}.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)
                    writer.writerows(rows)

    print("PostgreSQL data extraction complete.")


# MySQL Data Extraction and CSV Writing
def fetch_mysql_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password='root',
            database='WaterManagement'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Fetch all table names
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                # Write data to CSV
                with open(f"water_mysql_{table_name.lower()}.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)
                    writer.writerows(rows)

            print("MySQL data extraction complete.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            connection.close()


# MongoDB Data Extraction and CSV Writing
def fetch_mongodb_data():
    client = MongoClient(
        'not sharing')
    db = client['WaterManagement']

    collections = ["OptimizationTypes", "ContractStatuses", "CustomerRelevances", "ProgramTypes",
                   "WaterUsageOptimization", "Customer_ContractStatus", "CustomerDetails", "PoliciesDetails",
                   "ContractPolicies", "WaterConservationPrograms", "ConservationParticipants"]

    for collection_name in collections:
        collection = db[collection_name]
        documents = collection.find()

        # Convert documents to DataFrame and save to CSV
        df = pd.DataFrame(list(documents))

        # Write data to CSV
        df.to_csv(f"water_mongo_{collection_name.lower()}.csv", index=False)

    print("MongoDB data extraction complete.")


# Cassandra Data Extraction and CSV Writing
def fetch_cassandra_data():
    cluster = Cluster(["localhost"])
    session = cluster.connect("customer_contract_management")

    # Define tables to fetch data from
    tables = ["area_types", "classifications", "contract_statuses", "client_statuses", "clients", "contracts",
              "regulatory_policies", "contract_policies"]

    for table in tables:
        query = f"SELECT * FROM {table}"
        rows = session.execute(query)

        if rows:  # Check if the rows list is not empty
            # Write data to CSV
            with open(f"cassandra_{table}.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # Write column names from the first row
                writer.writerow(rows[0]._fields)
                for row in rows:
                    writer.writerow(row)
            print(f"Data from table {table} saved to CSV.")
        else:
            print(f"No data found for table {table}. Skipping CSV generation.")

    print("Cassandra data extraction complete.")


# Extract XML data from BaseX
def extract_xml_data():
    # Fetch the XML data from the BaseX database
    response = requests.get(
        f"{BASEX_URL}/{DATABASE_NAME}/documents.xml", auth=(USERNAME, PASSWORD)
    )
    if response.status_code != 200:
        print(f"Error fetching XML data: {response.status_code}")
        return None

    # Parse the XML data
    root = ET.fromstring(response.text)

    # Extract the relevant sections of the XML
    clients_data = []
    complaints_data = []
    membership_issues_data = []
    contract_breaches_data = []

    # Extract Clients
    clients = root.find("Clients")
    for client in clients.findall("Client"):
        client_data = {
            "ClientID": client.get("ClientID"),
            "Name": client.get("Name"),
            "Contact": client.get("Contact")
        }
        clients_data.append(client_data)

    # Extract Complaints
    complaints = root.find("Complaints")
    for complaint in complaints.findall("Complaint"):
        complaint_data = {
            "ComplaintID": complaint.get("ComplaintID"),
            "ClientID": complaint.get("ClientID"),
            "Type": complaint.get("Type"),
            "Date": complaint.get("Date"),
            "Status": complaint.get("Status")
        }
        complaints_data.append(complaint_data)

    # Extract Membership Issues
    membership_issues = root.find("MembershipIssues")
    for issue in membership_issues.findall("Issue"):
        issue_data = {
            "IssueID": issue.get("IssueID"),
            "ClientID": issue.get("ClientID"),
            "IssueType": issue.get("IssueType"),
            "Date": issue.get("Date"),
            "Status": issue.get("Status")
        }
        membership_issues_data.append(issue_data)

    # Extract Contract Breaches
    contract_breaches = root.find("ContractBreaches")
    for breach in contract_breaches.findall("Breach"):
        breach_data = {
            "BreachID": breach.get("BreachID"),
            "ClientID": breach.get("ClientID"),
            "Reason": breach.get("Reason"),
            "Date": breach.get("Date"),
            "Status": breach.get("Status")
        }
        contract_breaches_data.append(breach_data)

    return {
        "Clients": clients_data,
        "Complaints": complaints_data,
        "MembershipIssues": membership_issues_data,
        "ContractBreaches": contract_breaches_data
    }


# Save data to CSV files
def save_to_csv(data, table_name):
    if data:
        # Define CSV filename based on table name
        filename = f"{table_name.lower()}_xml.csv"

        # Define the headers for CSV based on the first entry
        headers = data[0].keys()

        # Open the CSV file for writing
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        print(f"Data saved to {filename}")
    else:
        print(f"No data available to save for {table_name}") 


class WaterQualityAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, data_type):
        # Append the type of data to the base URL
        url = f"{self.base_url}/{data_type}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
            return response.json()  # Return the JSON data as a Python object
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {data_type}: {e}")
            return None

    def save_to_csv(self, data, filename):
        if data:
            # Open the file in write mode
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()  # Write the header
                writer.writerows(data)  # Write all rows
            print(f"Data saved to {filename}")
        else:
            print("No data to save.")

# Example usage of the WaterQualityAPI class


def fetch_and_save_data():
    api = WaterQualityAPI("http://localhost:8081")

    # List of data types you want to fetch
    data_types = ['sensors', 'reports', 'temperature', 'ph', 'turbidity']

    # Iterate over each data type and fetch data
    for data_type in data_types:
        print(f"Fetching data for {data_type}...")
        data = api.get_data(data_type)

        if data:
            # Save the data to a CSV file
            api.save_to_csv(data, f"{data_type}.csv")
        else:
            print(f"No data found for {data_type}")


# Main Function to Run All Data Extractions
def main():
    fetch_postgres_data()
    fetch_mysql_data()
    fetch_mongodb_data()
    fetch_cassandra_data()
    fetch_and_save_data()

    # Extract data from the XML database
    data = extract_xml_data()

    # Save data to CSV files if data is available
    if data:
        save_to_csv(data.get("Clients"), "Clients")
        save_to_csv(data.get("Complaints"), "Complaints")
        save_to_csv(data.get("MembershipIssues"), "MembershipIssues")
        save_to_csv(data.get("ContractBreaches"), "ContractBreaches") 


if __name__ == "__main__":
    main()
