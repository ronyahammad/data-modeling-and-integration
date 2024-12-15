from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import uuid


def create_keyspace_and_tables():
    # Connect to Cassandra cluster
    cluster = Cluster(["localhost"])
    session = cluster.connect()

    # Create keyspace
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS customer_contract_management 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    # Use the created keyspace
    session.set_keyspace('customer_contract_management')

    # Create Clients Table
    session.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id UUID PRIMARY KEY,
        name TEXT,
        area_type TEXT,            -- Residential, Industrial, Business
        address TEXT,
        contact_number TEXT,
        classification TEXT,        -- Premium, General, Discount
        client_status_id UUID      -- Foreign key reference to client_status
    );
    """)

    # Create Contracts Table
    session.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        contract_id UUID PRIMARY KEY,
        client_id UUID,            -- Foreign key reference to clients (not enforced, manual handling)
        area_type TEXT,            -- Residential, Industrial, Business
        contract_type TEXT,        -- Premium, General, Discount
        start_date DATE,
        end_date DATE,
        status TEXT,               -- Active, Expired, Terminated, Breached
        base_fee DECIMAL,          -- Base fee associated with the contract
        last_updated TIMESTAMP,
        reason_for_status TEXT     -- Reason for breach or termination
    );
    """)

    # Create Regulatory Policies Table
    session.execute("""
    CREATE TABLE IF NOT EXISTS regulatory_policies (
        policy_id UUID PRIMARY KEY,
        policy_name TEXT,
        policy_details TEXT,
        effective_date DATE
    );
    """)

    # Create Contract Policies Table (for many-to-many relationships between contracts and policies)
    session.execute("""
    CREATE TABLE IF NOT EXISTS contract_policies (
        contract_id UUID,
        policy_id UUID,
        PRIMARY KEY (contract_id, policy_id)
    );
    """)

    # Create Client Status Table
    session.execute("""
    CREATE TABLE IF NOT EXISTS client_status (
        client_status_id UUID PRIMARY KEY,
        account_status TEXT       -- Enumeration for types of breaches or compliance issues
    );
    """)

    print("Keyspace and tables created successfully!")


if __name__ == "__main__":
    create_keyspace_and_tables()
