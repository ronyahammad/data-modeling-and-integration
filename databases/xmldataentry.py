import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

BASEX_URL = "http://localhost:8984/rest"
DATABASE_NAME = "customer_service_management"
USERNAME = "admin"
PASSWORD = "admin"


def create_database():
   
    response = requests.get(
        f"{BASEX_URL}/{DATABASE_NAME}", auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        print(f"Database '{DATABASE_NAME}' already exists.")
    else:
   
        response = requests.put(
            f"{BASEX_URL}/{DATABASE_NAME}", auth=(USERNAME, PASSWORD))
        if response.status_code == 201:
            print(f"Database '{DATABASE_NAME}' created successfully!")
        else:
            print(f"Error creating database: {response.status_code}")
            print(response.text)


def generate_clients():
    clients = ET.Element("Clients")
    for i in range(1, 401):  
        client = ET.SubElement(clients, "Client", {
            "ClientID": f"C{i}",
            "Name": f"Customer_{i}",
            "Contact": f"+3519100{str(i).zfill(4)}",
            "Address": f"Rua {i}, Faro",
            "AreaType": "Residential" if i <= 134 else ("Industrial" if i <= 267 else "Business")
        })
    return clients


def generate_complaints():
    complaints = ET.Element("Complaints")
    current_date = datetime.now()
    for i in range(1, 301):  
        complaint = ET.SubElement(complaints, "Complaint", {
            "ComplaintID": f"COMP{i}",
            "ClientID": f"C{(i % 400) + 1}",
            "Type": "Billing" if i % 3 == 0 else ("Contract Breach" if i % 3 == 1 else "Renewal"),
            "Date": (current_date - timedelta(days=i)).strftime("%Y-%m-%d"),
            "Status": "Pending" if i % 5 != 0 else ("Resolved" if i % 10 == 0 else "Under Review")
        })
    return complaints


def generate_membership_issues():
    membership_issues = ET.Element("MembershipIssues")
    current_date = datetime.now()
    for i in range(1, 201):  
        issue = ET.SubElement(membership_issues, "Issue", {
            "IssueID": f"ISS{i}",
            "ClientID": f"C{(i % 400) + 1}",
            "IssueType": "Membership Upgrade" if i % 2 == 0 else "Membership Downgrade",
            "Date": (current_date - timedelta(days=i * 2)).strftime("%Y-%m-%d"),
            "Status": "Pending" if i % 4 != 0 else "Resolved"
        })
    return membership_issues


def generate_contract_breaches():
    contract_breaches = ET.Element("ContractBreaches")
    current_date = datetime.now()
    for i in range(1, 151):  
        breach = ET.SubElement(contract_breaches, "Breach", {
            "BreachID": f"BR{i}",
            "ClientID": f"C{(i % 400) + 1}",
            "Reason": "Late Payment" if i % 2 == 0 else "Policy Violation",
            "Date": (current_date - timedelta(days=i * 3)).strftime("%Y-%m-%d"),
            "Status": "Under Review" if i % 3 != 0 else "Resolved"
        })
    return contract_breaches


def create_sample_data():
    
    root = ET.Element("CustomerServiceManagement")

    
    root.append(generate_clients())
    root.append(generate_complaints())
    root.append(generate_membership_issues())
    root.append(generate_contract_breaches())

    
    xml_data = ET.tostring(root, encoding='unicode')

    
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
