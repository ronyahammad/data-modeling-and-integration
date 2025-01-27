import psycopg2


def create_database():
    conn_params = {
        "dbname": "admin",
        "user": "postgres",
        "password": "admin",
        "host": "localhost",
        "port": 5433
    }

    sql_schema = """
    -- Drop existing tables to avoid duplication errors
    DROP TABLE IF EXISTS BillingDetails;
    DROP TABLE IF EXISTS BillingRecords;
    DROP TABLE IF EXISTS WasteDisposal;
    DROP TABLE IF EXISTS CollectionSchedule;
    DROP TABLE IF EXISTS Clients_list;
    DROP TABLE IF EXISTS WasteCategories;
    DROP TABLE IF EXISTS AreaTypes;
    DROP TABLE IF EXISTS CollectionFrequencies;

    CREATE TABLE AreaTypes (
        AreaTypeID SERIAL PRIMARY KEY,
        AreaType VARCHAR(20) UNIQUE NOT NULL,
        Description VARCHAR(255) NOT NULL
    );

    CREATE TABLE CollectionFrequencies (
        FrequencyID SERIAL PRIMARY KEY,
        CollectionFrequency VARCHAR(20) UNIQUE NOT NULL,
        Description VARCHAR(255) NOT NULL
    );

    CREATE TABLE Clients_list (
        ClientID SERIAL PRIMARY KEY,
        Name VARCHAR(100) NOT NULL,
        fullAddress VARCHAR(255) NOT NULL,
        Postcode VARCHAR(20) NOT NULL,
        AreaTypeID INT NOT NULL,
        mobileInfo VARCHAR(100) NOT NULL,
        FOREIGN KEY (AreaTypeID) REFERENCES AreaTypes(AreaTypeID)
    );

    CREATE TABLE WasteCategories (
        WasteCategoryID SERIAL PRIMARY KEY,
        WasteType VARCHAR(50) NOT NULL,
        UnitPricePerKg DECIMAL(10, 2) NOT NULL,
        Description VARCHAR(255)
    );

    CREATE INDEX idx_wastetype ON WasteCategories (WasteType);

    CREATE TABLE CollectionSchedule (
        ClientID INT NOT NULL,
        WasteCategoryID INT NOT NULL,
        FrequencyID INT NOT NULL,
        LastCollectionDate DATE,
        NextCollectionDate DATE,
        PRIMARY KEY (ClientID, WasteCategoryID, FrequencyID),
        FOREIGN KEY (ClientID) REFERENCES Clients_list(ClientID),
        FOREIGN KEY (WasteCategoryID) REFERENCES WasteCategories(WasteCategoryID),
        FOREIGN KEY (FrequencyID) REFERENCES CollectionFrequencies(FrequencyID)
    );

    CREATE TABLE WasteDisposal (
        DisposalID SERIAL PRIMARY KEY,
        ClientID INT NOT NULL,
        WasteCategoryID INT NOT NULL,
        FrequencyID INT NOT NULL,
        DisposalDate DATE NOT NULL,
        QuantityInKg DECIMAL(10, 2) NOT NULL CHECK (QuantityInKg <= 5000),
        FOREIGN KEY (ClientID, WasteCategoryID, FrequencyID) 
            REFERENCES CollectionSchedule(ClientID, WasteCategoryID, FrequencyID)
    );

    CREATE TABLE BillingRecords (
        BillingID SERIAL PRIMARY KEY,
        ClientID INT NOT NULL,
        BillingDate DATE NOT NULL,
        TotalAmount DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (ClientID) REFERENCES Clients_list(ClientID)
    );

    CREATE TABLE BillingDetails (
        BillingDetailID SERIAL PRIMARY KEY,
        BillingID INT NOT NULL,
        WasteCategoryID INT NOT NULL,
        QuantityInKg DECIMAL(10, 2) NOT NULL,
        SubTotal DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (BillingID) REFERENCES BillingRecords(BillingID),
        FOREIGN KEY (WasteCategoryID) REFERENCES WasteCategories(WasteCategoryID)
    );

    -- Insert default values into AreaTypes
    INSERT INTO AreaTypes (AreaType, Description) VALUES
        ('Residential', 'Areas primarily for housing and residential purposes'),
        ('Industrial', 'Zones designated for industrial facilities and factories'),
        ('Business', 'Commercial and business-related areas');

    -- Insert default values into CollectionFrequencies
    INSERT INTO CollectionFrequencies (CollectionFrequency, Description) VALUES
        ('Daily', 'Collection occurs every day'),
        ('Weekly', 'Collection occurs once a week'),
        ('Bi-Weekly', 'Collection occurs every two weeks'),
        ('Monthly', 'Collection occurs once a month');
    """

    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_schema)
                print(
                    "Database tables created successfully !")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_database()
