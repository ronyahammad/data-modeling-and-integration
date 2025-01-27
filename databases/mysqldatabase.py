import mysql.connector
from mysql.connector import Error


def create_database():
    try:
        
        connection = mysql.connector.connect(
            host='localhost',  
            port=3307,          
            user='root',       
            password='root'    
        )

        if connection.is_connected():
            cursor = connection.cursor()

           
            cursor.execute("DROP DATABASE IF EXISTS `WaterManagement`;")
            print("Existing database 'WaterManagement' deleted if it existed.")

           
            cursor.execute(
                "CREATE SCHEMA `WaterManagement` DEFAULT CHARACTER SET utf8;")
            print("Database 'WaterManagement' created.")

         
            cursor.execute("USE `WaterManagement`;")

            
            sql_script = """
                -- Table for Program Types (used in WaterConservationPrograms)
                CREATE TABLE IF NOT EXISTS `ProgramTypes` (
                  `ProgramTypeID` INT NOT NULL AUTO_INCREMENT,
                  `Description` VARCHAR(100) NOT NULL,
                  PRIMARY KEY (`ProgramTypeID`)
                );

                -- Table for Water Conservation Programs
                CREATE TABLE IF NOT EXISTS `WaterConservationPrograms` (
                  `ProgramID` INT NOT NULL AUTO_INCREMENT,
                  `ProgramName` VARCHAR(100) NOT NULL,
                  `ProgramTypeID` INT NOT NULL,
                  `StartDate` DATE NOT NULL,
                  `EndDate` DATE NOT NULL,
                  PRIMARY KEY (`ProgramID`),
                  CONSTRAINT `fk_WaterConservationPrograms_ProgramTypes`
                    FOREIGN KEY (`ProgramTypeID`)
                    REFERENCES `ProgramTypes` (`ProgramTypeID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );

                -- Table for Water Sources
                CREATE TABLE IF NOT EXISTS `WaterSource` (
                  `SourceID` INT NOT NULL AUTO_INCREMENT,
                  `SourceType` VARCHAR(50) NOT NULL,
                  `Location` VARCHAR(100) NOT NULL,
                  `Capacity` FLOAT NOT NULL,
                  PRIMARY KEY (`SourceID`)
                );

                -- Table for Departments
                CREATE TABLE IF NOT EXISTS `Departments` (
                  `DepartmentID` INT NOT NULL AUTO_INCREMENT,
                  `DepartmentName` VARCHAR(100) NOT NULL,
                  `SourceID` INT NOT NULL,
                  PRIMARY KEY (`DepartmentID`),
                  CONSTRAINT `fk_Departments_WaterSource` 
                    FOREIGN KEY (`SourceID`)
                    REFERENCES `WaterSource` (`SourceID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );

                -- Table for Water Usage Records
                CREATE TABLE IF NOT EXISTS `WaterUsageRecords` (
                  `UsageID` INT NOT NULL AUTO_INCREMENT,
                  `DepartmentID` INT NOT NULL,
                  `SourceID` INT NOT NULL,  -- Added SourceID to link WaterUsageRecords to WaterSource
                  `UsageDate` DATE NOT NULL,
                  `VolumeUsed` FLOAT NOT NULL,
                  `Purpose` VARCHAR(100) NOT NULL,
                  PRIMARY KEY (`UsageID`),
                  CONSTRAINT `fk_WaterUsageRecords_Departments` 
                    FOREIGN KEY (`DepartmentID`) 
                    REFERENCES `Departments` (`DepartmentID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                  CONSTRAINT `fk_WaterUsageRecords_WaterSource`
                    FOREIGN KEY (`SourceID`) 
                    REFERENCES `WaterSource` (`SourceID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );

                -- Table for Treatment Equipment
                CREATE TABLE IF NOT EXISTS `TreatmentEquipment` (
                  `EquipmentID` INT NOT NULL AUTO_INCREMENT,
                  `EquipmentName` VARCHAR(100) NOT NULL,
                  `SourceID` INT NOT NULL,
                  `LastInspectionDate` DATE NOT NULL,
                  PRIMARY KEY (`EquipmentID`),
                  CONSTRAINT `fk_TreatmentEquipment_WaterSource` 
                    FOREIGN KEY (`SourceID`) 
                    REFERENCES `WaterSource` (`SourceID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );

                -- Table for Maintenance Logs
                CREATE TABLE IF NOT EXISTS `MaintenanceLogs` (
                  `LogID` INT NOT NULL AUTO_INCREMENT,
                  `EquipmentID` INT NOT NULL,
                  `MaintenanceDate` DATE NOT NULL,
                  `PartsReplaced` VARCHAR(200) NOT NULL,
                  `TechnicianNotes` TEXT NULL,
                  PRIMARY KEY (`LogID`),
                  CONSTRAINT `fk_MaintenanceLogs_TreatmentEquipment` 
                    FOREIGN KEY (`EquipmentID`) 
                    REFERENCES `TreatmentEquipment` (`EquipmentID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );

                -- Table for Water Quality Tests
                CREATE TABLE IF NOT EXISTS `WaterQualityTests` (
                  `TestID` INT NOT NULL AUTO_INCREMENT,
                  `SourceID` INT NOT NULL,
                  `TestDate` DATE NOT NULL,
                  `TestResults` TEXT NOT NULL,
                  PRIMARY KEY (`TestID`),
                  CONSTRAINT `fk_WaterQualityTests_WaterSource` 
                    FOREIGN KEY (`SourceID`) 
                    REFERENCES `WaterSource` (`SourceID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );

                -- Table for Customers
                CREATE TABLE IF NOT EXISTS `CustomerDetails` (
                  `CustomerID` INT NOT NULL AUTO_INCREMENT,
                  `Name` VARCHAR(150) NOT NULL,
                  `ConsumerType` VARCHAR(45) NOT NULL,
                  `Address` VARCHAR(250) NOT NULL,
                  `ContactInfo` VARCHAR(45) NOT NULL,
                  PRIMARY KEY (`CustomerID`)
                );

                -- Table for Customer Participation in Water Conservation Programs
                CREATE TABLE IF NOT EXISTS `CustomerConservationPrograms` (
                  `ParticipationID` INT NOT NULL AUTO_INCREMENT,
                  `CustomerID` INT NOT NULL,
                  `ProgramID` INT NOT NULL,
                  `ParticipationStartDate` DATE NOT NULL,
                  PRIMARY KEY (`ParticipationID`),
                  CONSTRAINT `fk_CustomerConservationPrograms_Customers`
                    FOREIGN KEY (`CustomerID`)
                    REFERENCES `CustomerDetails` (`CustomerID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                  CONSTRAINT `fk_CustomerConservationPrograms_WaterConservationPrograms`
                    FOREIGN KEY (`ProgramID`)
                    REFERENCES `WaterConservationPrograms` (`ProgramID`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );
            """

          
            for statement in sql_script.split(";"):
                if statement.strip():
                    cursor.execute(statement)

            
            cursor.execute("ALTER TABLE `WaterSource` AUTO_INCREMENT = 1;")
            print("AUTO_INCREMENT for WaterSource set to 1.")

            print("Database and tables created successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")



if __name__ == "__main__":
    create_database()
