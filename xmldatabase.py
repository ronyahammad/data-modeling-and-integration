import requests
import xml.etree.ElementTree as ET

BASEX_URL = "http://localhost:8984/rest"
DATABASE_NAME = "customer_service_management"
USERNAME = "admin"
PASSWORD = "admin"


def create_database():
    # Check if the database already exists
    response = requests.get(
        f"{BASEX_URL}/{DATABASE_NAME}", auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        print(f"Database '{DATABASE_NAME}' already exists.")
    else:
        # Create the database
        response = requests.put(
            f"{BASEX_URL}/{DATABASE_NAME}", auth=(USERNAME, PASSWORD))
        if response.status_code == 201:
            print(f"Database '{DATABASE_NAME}' created successfully!")
        else:
            print(f"Error creating database: {response.status_code}")
            print(response.text)


def create_sample_data():
    # Define the root XML structure
    root = ET.Element("CustomerServiceManagement")

    # Clients section
    clients = ET.SubElement(root, "Clients")
    ET.SubElement(clients, "Client", {
                  "ClientID": "", "Name": "", "Contact": ""})

    # Complaints section
    complaints = ET.SubElement(root, "Complaints")
    ET.SubElement(complaints, "Complaint", {
                  "ComplaintID": "", "ClientID": "", "Type": "", "Date": "", "Status": ""})

    # Membership Issues section
    membership_issues = ET.SubElement(root, "MembershipIssues")
    ET.SubElement(membership_issues, "Issue", {
                  "IssueID": "", "ClientID": "", "IssueType": "", "Date": "", "Status": ""})

    # Contract Breaches section
    contract_breaches = ET.SubElement(root, "ContractBreaches")
    ET.SubElement(contract_breaches, "Breach", {
                  "BreachID": "", "ClientID": "", "Reason": "", "Date": "", "Status": ""})

    # Convert XML tree to string
    xml_data = ET.tostring(root, encoding='unicode')

    # Store the XML data in the database
    response = requests.put(
        f"{BASEX_URL}/{DATABASE_NAME}/documents.xml", data=xml_data, auth=(USERNAME, PASSWORD))
    if response.status_code in (201, 204):
        print("Sample data added successfully!")
    else:
        print(f"Error adding sample data: {response.status_code}")
        print(response.text)


def main():
    create_database()
    create_sample_data()


if __name__ == "__main__":
    main()
