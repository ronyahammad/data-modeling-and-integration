from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import uuid


def create_keyspace_and_tables():
    
    cluster = Cluster(["localhost"])
    session = cluster.connect()

    
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS customer_contract_management 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    
    session.set_keyspace('customer_contract_management')

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS area_types (
        area_type_id UUID PRIMARY KEY,
        area_type TEXT,
        description TEXT
    );
    """)

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS classifications (
        classification_id UUID PRIMARY KEY,
        classification TEXT,
        description TEXT
    );
    """)

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS contract_statuses (
        status_id UUID PRIMARY KEY,
        status TEXT,
        description TEXT
    );
    """)

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS client_statuses (
        client_status_id UUID PRIMARY KEY,
        account_status TEXT,
        description TEXT
    );
    """)

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id UUID PRIMARY KEY,
        name TEXT,
        area_type_id UUID,         -- Foreign key reference to area_types
        address TEXT,
        contact_number TEXT,
        classification_id UUID,   -- Foreign key reference to classifications
        client_status_id UUID     -- Foreign key reference to client_statuses
    );
    """)

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        contract_id UUID PRIMARY KEY,
        client_id UUID,            -- Foreign key reference to clients (manual handling)
        area_type_id UUID,         -- Foreign key reference to area_types
        contract_type_id UUID,     -- Foreign key reference to classifications
        start_date DATE,
        end_date DATE,
        status_id UUID,            -- Foreign key reference to contract_statuses
        base_fee DECIMAL,          -- Base fee associated with the contract
        last_updated TIMESTAMP,
        reason_for_status TEXT     -- Reason for breach or termination
    );
    """)

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS regulatory_policies (
        policy_id UUID PRIMARY KEY,
        policy_name TEXT,
        policy_details TEXT,
        effective_date DATE
    );
    """)

    
    session.execute("""
    CREATE TABLE IF NOT EXISTS contract_policies (
        contract_id UUID,
        policy_id UUID,
        PRIMARY KEY (contract_id, policy_id)
    );
    """)

    print("Keyspace and tables created successfully!")


if __name__ == "__main__":
    create_keyspace_and_tables()
