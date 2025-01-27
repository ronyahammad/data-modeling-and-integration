from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import uuid


def populate_database():
  
    cluster = Cluster(["localhost"])
    session = cluster.connect()
    session.set_keyspace('customer_contract_management')

    
    session.execute("TRUNCATE area_types")
    session.execute("TRUNCATE classifications")
    session.execute("TRUNCATE client_statuses")
    session.execute("TRUNCATE contract_statuses")
    session.execute("TRUNCATE clients")
    session.execute("TRUNCATE contracts")
    session.execute("TRUNCATE regulatory_policies")
    session.execute("TRUNCATE contract_policies")

    
    area_types = [
        (uuid.uuid4(), "Residential", "Residential area for housing"),
        (uuid.uuid4(), "Industrial", "Industrial zones with factories"),
        (uuid.uuid4(), "Business", "Business and commercial areas")
    ]
    for area_type in area_types:
        session.execute("""
        INSERT INTO area_types (area_type_id, area_type, description)
        VALUES (%s, %s, %s)
        """, area_type)

    
    area_type_map = {area_type[1]: area_type[0] for area_type in area_types}


    classifications = [
        (uuid.uuid4(), "Premium", "Premium level clients"),
        (uuid.uuid4(), "General", "General level clients"),
        (uuid.uuid4(), "Discount", "Clients with discount benefits")
    ]
    for classification in classifications:
        session.execute("""
        INSERT INTO classifications (classification_id, classification, description)
        VALUES (%s, %s, %s)
        """, classification)

    
    classification_map = {
        classification[1]: classification[0] for classification in classifications}


    client_statuses = [
        (uuid.uuid4(), "No Breach", "Client is in good standing"),
        (uuid.uuid4(), "Payment Delay", "Client has delayed payment"),
        (uuid.uuid4(), "Contract Breach", "Client has breached contract terms"),
        (uuid.uuid4(), "Compliance Issue", "Client has compliance-related issues")
    ]
    for status in client_statuses:
        session.execute("""
        INSERT INTO client_statuses (client_status_id, account_status, description)
        VALUES (%s, %s, %s)
        """, status)


    client_status_map = {status[1]: status[0] for status in client_statuses}


    contract_statuses = [
        (uuid.uuid4(), "Active", "The contract is currently active and ongoing"),
        (uuid.uuid4(), "Expired", "The contract has expired but may be renewed"),
        (uuid.uuid4(), "Suspended", "The contract is temporarily suspended"),
        (uuid.uuid4(), "Terminated", "The contract has been terminated")
    ]
    for status in contract_statuses:
        session.execute("""
        INSERT INTO contract_statuses (status_id, status, description)
        VALUES (%s, %s, %s)
        """, status)


    contract_status_map = {status[1]: status[0]
                           for status in contract_statuses}


    clients = []
    for i in range(1, 201):
        client_id = uuid.uuid4()
        name = f"Customer_{i}"
        address = f"Rua {i}, Faro"
        if i <= 67:
            area_type = "Residential"
            contact_number = f"+3519100{str(i).zfill(4)}"
            classification = "General"
        elif i <= 134:
            area_type = "Industrial"
            contact_number = f"+3519200{str(i - 67).zfill(4)}"
            classification = "Premium"
        else:
            area_type = "Business"
            contact_number = f"+3519300{str(i - 134).zfill(4)}"
            classification = "Discount"
        client_status_id = list(client_status_map.values())[
            i % len(client_status_map)]
        clients.append((client_id, name, area_type_map[area_type], address,
                       contact_number, classification_map[classification], client_status_id))

    for client in clients:
        session.execute("""
        INSERT INTO clients (client_id, name, area_type_id, address, contact_number, classification_id, client_status_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, client)

    contracts = []
    current_date = datetime.now()
    for idx, client in enumerate(clients):
        contract_id = uuid.uuid4()
        client_id = client[0]
        area_type_id = client[2]
        classification_id = client[5]
        start_date = (current_date - timedelta(days=365)).date()
        end_date = (current_date + timedelta(days=365)).date()
        status = list(contract_status_map.values())[idx % len(
            contract_status_map)]  
        base_fee = 100.00
        last_updated = current_date
        reason_for_status = None
        contracts.append((contract_id, client_id, area_type_id, classification_id,
                         start_date, end_date, status, base_fee, last_updated, reason_for_status))

    for contract in contracts:
        session.execute("""
        INSERT INTO contracts (contract_id, client_id, area_type_id, contract_type_id, start_date, end_date, status_id, base_fee, last_updated, reason_for_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, contract)

  
    policies = [
        (uuid.uuid4(), "Policy 1", "Details of policy 1", current_date.date()),
        (uuid.uuid4(), "Policy 2", "Details of policy 2", current_date.date()),
        (uuid.uuid4(), "Policy 3", "Details of policy 3", current_date.date())
    ]
    for policy in policies:
        session.execute("""
        INSERT INTO regulatory_policies (policy_id, policy_name, policy_details, effective_date)
        VALUES (%s, %s, %s, %s)
        """, policy)


    contract_policies = []
    for contract in contracts:
        for policy in policies:
            contract_policies.append((contract[0], policy[0]))

    for cp in contract_policies:
        session.execute("""
        INSERT INTO contract_policies (contract_id, policy_id)
        VALUES (%s, %s)
        """, cp)

    print("Database populated successfully!")


if __name__ == "__main__":
    populate_database()
