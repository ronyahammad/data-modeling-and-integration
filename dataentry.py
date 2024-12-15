from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import uuid


def populate_database():
    # Connect to Cassandra cluster
    cluster = Cluster(["localhost"])
    session = cluster.connect()
    session.set_keyspace('customer_contract_management')

    # Populate Clients Table
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
        client_status_id = uuid.uuid4()
        clients.append((client_id, name, area_type, address,
                       contact_number, classification, client_status_id))

    for client in clients:
        session.execute("""
        INSERT INTO clients (client_id, name, area_type, address, contact_number, classification, client_status_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, client)

    # Populate Contracts Table
    contracts = []
    current_date = datetime.now()
    for client in clients:
        contract_id = uuid.uuid4()
        client_id = client[0]
        area_type = client[2]
        contract_type = client[5]
        start_date = (current_date - timedelta(days=365)
                      ).date()  # Convert to date
        end_date = (current_date + timedelta(days=365)
                    ).date()    # Convert to date
        status = "Active"
        base_fee = 100.00
        last_updated = current_date  # Keep as datetime for timestamp
        reason_for_status = None
        contracts.append((contract_id, client_id, area_type, contract_type,
                         start_date, end_date, status, base_fee, last_updated, reason_for_status))

    for contract in contracts:
        session.execute("""
        INSERT INTO contracts (contract_id, client_id, area_type, contract_type, start_date, end_date, status, base_fee, last_updated, reason_for_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, contract)

    # Populate Regulatory Policies Table
    policies = [
        (uuid.uuid4(), "Policy 1", "Details of policy 1",
         current_date.date()),  # Convert to date
        (uuid.uuid4(), "Policy 2", "Details of policy 2",
         current_date.date()),  # Convert to date
        (uuid.uuid4(), "Policy 3", "Details of policy 3",
         current_date.date())   # Convert to date
    ]
    for policy in policies:
        session.execute("""
        INSERT INTO regulatory_policies (policy_id, policy_name, policy_details, effective_date)
        VALUES (%s, %s, %s, %s)
        """, policy)

    # Populate Contract Policies Table
    contract_policies = []
    for contract in contracts:
        for policy in policies:
            contract_policies.append((contract[0], policy[0]))

    for cp in contract_policies:
        session.execute("""
        INSERT INTO contract_policies (contract_id, policy_id)
        VALUES (%s, %s)
        """, cp)

    # Populate Client Status Table
    statuses = [("No Breach",), ("Payment Delay",),
                ("Contract Breach",), ("Compliance Issue",)]
    for client in clients:
        client_status_id = client[-1]
        account_status = statuses[(clients.index(client) % len(statuses))][0]
        session.execute("""
        INSERT INTO client_status (client_status_id, account_status)
        VALUES (%s, %s)
        """, (client_status_id, account_status))

    print("Database populated successfully!")


if __name__ == "__main__":
    populate_database()
