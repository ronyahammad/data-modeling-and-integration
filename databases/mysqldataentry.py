import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta


def populate_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password='root',
            database='WaterManagement'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Step 1: Populate WaterSource table
            water_sources = [
                ('Reservoir', 'North Zone', 10000.0),
                ('Lake', 'East Zone', 8000.0),
                ('River', 'South Zone', 12000.0),
                ('Well', 'West Zone', 5000.0),
                ('Spring', 'Central Zone', 7000.0),
            ]
            cursor.executemany(
                "INSERT INTO WaterSource (SourceType, Location, Capacity) VALUES (%s, %s, %s)", water_sources)
            connection.commit()

            # Fetch SourceIDs from WaterSource table after insertion
            cursor.execute(
                "SELECT SourceID FROM WaterSource ORDER BY SourceID")
            source_ids = [row[0] for row in cursor.fetchall()]

            # Step 2: Populate Departments table using fetched SourceIDs
            departments = [
                ('Water Distribution', source_ids[0]),
                ('Irrigation', source_ids[1]),
                ('Industrial Supply', source_ids[2]),
                ('Agriculture', source_ids[3]),
                ('Public Supply', source_ids[4])
            ]
            cursor.executemany(
                "INSERT INTO Departments (DepartmentName, SourceID) VALUES (%s, %s)", departments)
            connection.commit()

            # Fetch DepartmentIDs from Departments table
            cursor.execute(
                "SELECT DepartmentID FROM Departments ORDER BY DepartmentID")
            department_ids = [row[0] for row in cursor.fetchall()]

            # Step 3: Populate CustomerDetails table
            customers = []
            for i in range(1, 1001):
                name = f"Customer_{i}"
                consumer_type = "Residential" if i <= 400 else "Industrial" if i <= 800 else "Business"
                full_address = f"Rua {i}, CityZone"
                contact_info = f"+35191000{i:04d}"
                customers.append(
                    (name, consumer_type, full_address, contact_info)
                )

            cursor.executemany(
                "INSERT INTO CustomerDetails (Name, ConsumerType, Address, ContactInfo) VALUES (%s, %s, %s, %s)", customers)
            connection.commit()

            # Fetch CustomerIDs from CustomerDetails table
            cursor.execute(
                "SELECT CustomerID FROM CustomerDetails ORDER BY CustomerID")
            customer_ids = [row[0] for row in cursor.fetchall()]

            # Step 4: Populate WaterUsageRecords table
            usage_records = []
            start_date = date.today() - timedelta(days=5 * 365)  # 5 years ago
            for i in range(1, 5001):
                department_id = department_ids[(i - 1) % len(department_ids)]
                source_id = source_ids[(i - 1) % len(source_ids)]
                usage_date = start_date + \
                    timedelta(days=(i % 1825))  # Spread over 5 years
                volume_used = 150 + (i % 100)  # Logical volume pattern
                purpose = f"Purpose_{(i % 5) + 1}"
                usage_records.append(
                    (department_id, source_id, usage_date, volume_used, purpose)
                )

            cursor.executemany(
                "INSERT INTO WaterUsageRecords (DepartmentID, SourceID, UsageDate, VolumeUsed, Purpose) VALUES (%s, %s, %s, %s, %s)", usage_records)
            connection.commit()

            # Step 5: Populate TreatmentEquipment table
            treatment_equipment = []
            for i in range(1, 51):
                equipment_name = f"Treatment Equipment {i}"
                source_id = source_ids[(i - 1) % len(source_ids)]
                last_inspection_date = start_date + timedelta(days=(i % 365))
                treatment_equipment.append(
                    (equipment_name, source_id, last_inspection_date)
                )

            cursor.executemany(
                "INSERT INTO TreatmentEquipment (EquipmentName, SourceID, LastInspectionDate) VALUES (%s, %s, %s)", treatment_equipment)
            connection.commit()

            # Fetch EquipmentIDs from TreatmentEquipment table
            cursor.execute(
                "SELECT EquipmentID FROM TreatmentEquipment ORDER BY EquipmentID")
            equipment_ids = [row[0] for row in cursor.fetchall()]

            # Step 6: Populate MaintenanceLogs table
            maintenance_logs = []
            for i in range(1, 1001):
                equipment_id = equipment_ids[(i - 1) % len(equipment_ids)]
                maintenance_date = start_date + timedelta(days=(i * 3) % 365)
                parts_replaced = f"Part_{(i % 5) + 1}"
                technician_notes = f"Technician note {i}"
                maintenance_logs.append(
                    (equipment_id, maintenance_date,
                     parts_replaced, technician_notes)
                )

            cursor.executemany(
                "INSERT INTO MaintenanceLogs (EquipmentID, MaintenanceDate, PartsReplaced, TechnicianNotes) VALUES (%s, %s, %s, %s)", maintenance_logs)
            connection.commit()

            # Step 7: Populate WaterQualityTests table
            water_quality_tests = []
            for i in range(1, 1001):
                source_id = source_ids[(i - 1) % len(source_ids)]
                test_date = start_date + timedelta(days=(i % 365))
                test_results = f"Test result {i % 5 + 1}"
                water_quality_tests.append(
                    (source_id, test_date, test_results)
                )

            cursor.executemany(
                "INSERT INTO WaterQualityTests (SourceID, TestDate, TestResults) VALUES (%s, %s, %s)", water_quality_tests)
            connection.commit()

            # Step 8: Populate WaterConservationPrograms table
            program_types = [
                ('Education',),
                ('Sustainability',),
                ('Research',)
            ]
            cursor.executemany(
                "INSERT INTO ProgramTypes (Description) VALUES (%s)", program_types)
            connection.commit()

            # Fetch ProgramTypeIDs from ProgramTypes table
            cursor.execute(
                "SELECT ProgramTypeID FROM ProgramTypes ORDER BY ProgramTypeID")
            program_type_ids = [row[0] for row in cursor.fetchall()]

            water_conservation_programs = []
            for i in range(1, 501):
                program_name = f"Program {i}"
                program_type_id = program_type_ids[(
                    i - 1) % len(program_type_ids)]
                start_date = date(2024, 1, 1)
                end_date = date(2025, 1, 1)
                water_conservation_programs.append(
                    (program_name, program_type_id, start_date, end_date)
                )

            cursor.executemany(
                "INSERT INTO WaterConservationPrograms (ProgramName, ProgramTypeID, StartDate, EndDate) VALUES (%s, %s, %s, %s)", water_conservation_programs)
            connection.commit()

            # Fetch ProgramIDs from WaterConservationPrograms table
            cursor.execute(
                "SELECT ProgramID FROM WaterConservationPrograms ORDER BY ProgramID")
            program_ids = [row[0] for row in cursor.fetchall()]

            # Step 9: Populate CustomerConservationPrograms table
            conservation_participants = []
            for i in range(1, 1001):
                customer_id = customer_ids[(i - 1) % len(customer_ids)]
                program_id = program_ids[(i - 1) % len(program_ids)]
                participation_start_date = date(2024, 1, 1)
                conservation_participants.append(
                    (customer_id, program_id, participation_start_date)
                )

            cursor.executemany(
                "INSERT INTO CustomerConservationPrograms (CustomerID, ProgramID, ParticipationStartDate) VALUES (%s, %s, %s)", conservation_participants)
            connection.commit()

            print("Database populated successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


# Call the function to populate the database
if __name__ == "__main__":
    populate_database()
