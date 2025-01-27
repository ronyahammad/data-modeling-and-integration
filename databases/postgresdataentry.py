import psycopg2
import datetime


def populate_database():
    conn_params = {
        "dbname": "admin",
        "user": "postgres",
        "password": "admin",
        "host": "localhost",
        "port": 5433
    }

    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Retrieve valid AreaTypeIDs
                cursor.execute("SELECT AreaTypeID, AreaType FROM AreaTypes")
                area_types = {row[1]: row[0] for row in cursor.fetchall()}

                # Retrieve valid FrequencyIDs
                cursor.execute(
                    "SELECT FrequencyID, CollectionFrequency FROM CollectionFrequencies")
                collection_frequencies = {row[1]: row[0]
                                          for row in cursor.fetchall()}

                # Populate WasteCategories
                waste_categories = [
                    ("Organic", 0.5, "Biodegradable waste"),
                    ("Hazardous", 1.5, "Chemicals, batteries, etc."),
                    ("Recyclable", 0.3, "Paper, plastic, etc."),
                    ("General", 0.8, "Mixed waste")
                ]
                cursor.executemany("""
                    INSERT INTO WasteCategories (WasteType, UnitPricePerKg, Description)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, waste_categories)
                conn.commit()

                # Retrieve valid WasteCategoryIDs
                cursor.execute("SELECT WasteCategoryID FROM WasteCategories")
                valid_waste_category_ids = [row[0]
                                            for row in cursor.fetchall()]

                # Populate Clients_list
                customers = []
                for i in range(1, 201):
                    name = f"Customer_{i}"
                    rua_code = f"{i:02}"

                    if i <= 67:
                        area_type = "Residential"
                        postcode = f"8{rua_code}-00{i % 1000:03}"
                        mobile_info = f"+3519100{str(i).zfill(4)}"
                    elif i <= 134:
                        area_type = "Industrial"
                        postcode = f"9{rua_code}-00{i % 1000:03}"
                        mobile_info = f"+3519200{str(i - 67).zfill(4)}"
                    else:
                        area_type = "Business"
                        postcode = f"7{rua_code}-00{i % 1000:03}"
                        mobile_info = f"+3519300{str(i - 134).zfill(4)}"

                    full_address = f"rua {i}, Faro"
                    area_type_id = area_types[area_type]
                    customers.append(
                        (name, full_address, postcode, area_type_id, mobile_info))

                cursor.executemany("""
                    INSERT INTO Clients_list (Name, fullAddress, Postcode, AreaTypeID, mobileInfo)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, customers)
                conn.commit()

                # Retrieve valid ClientIDs
                cursor.execute("SELECT ClientID FROM Clients_list")
                valid_client_ids = [row[0] for row in cursor.fetchall()]

                # Populate CollectionSchedule
                schedules = []
                current_date = datetime.datetime.now()
                for client_id in valid_client_ids:
                    for waste_category_id in valid_waste_category_ids:
                        if client_id <= 67:
                            frequency = "Daily"
                        elif client_id <= 134:
                            frequency = "Weekly"
                        else:
                            frequency = "Bi-Weekly"

                        frequency_id = collection_frequencies[frequency]
                        last_collection_date = current_date - \
                            datetime.timedelta(days=client_id % 30)
                        next_collection_date = last_collection_date + datetime.timedelta(days={
                            "Daily": 1,
                            "Weekly": 7,
                            "Bi-Weekly": 14
                        }[frequency])
                        schedules.append((client_id, waste_category_id, frequency_id,
                                          last_collection_date.date(), next_collection_date.date()))

                cursor.executemany("""
                    INSERT INTO CollectionSchedule (ClientID, WasteCategoryID, FrequencyID, LastCollectionDate, NextCollectionDate)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, schedules)
                conn.commit()

                # Retrieve valid CollectionSchedule records
                cursor.execute("""
                    SELECT ClientID, WasteCategoryID, FrequencyID 
                    FROM CollectionSchedule
                """)
                valid_schedules = cursor.fetchall()

                # Populate WasteDisposal based on valid CollectionSchedule entries
                waste_disposal_records = []
                for i, (client_id, waste_category_id, frequency_id) in enumerate(valid_schedules):
                    disposal_date = current_date - \
                        datetime.timedelta(days=i % 730)
                    quantity = round(((i + 1) % 5000) / 10, 2)
                    waste_disposal_records.append(
                        (client_id, waste_category_id, frequency_id,
                         disposal_date.date(), quantity)
                    )

                cursor.executemany("""
                    INSERT INTO WasteDisposal (ClientID, WasteCategoryID, FrequencyID, DisposalDate, QuantityInKg)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, waste_disposal_records)
                conn.commit()

                # Populate BillingRecords
                billing_records = []
                for client_id in valid_client_ids:
                    # For simplicity, assuming that the total amount is a multiple of the waste categories and the quantity
                    total_amount = sum(
                        0.5 * i for i in range(1, len(valid_waste_category_ids) + 1))
                    billing_date = current_date - \
                        datetime.timedelta(days=client_id % 30)
                    billing_records.append(
                        (client_id, billing_date.date(), round(total_amount, 2)))

                cursor.executemany("""
                    INSERT INTO BillingRecords (ClientID, BillingDate, TotalAmount)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, billing_records)
                conn.commit()

                # Retrieve valid BillingIDs
                cursor.execute(
                    "SELECT BillingID, ClientID FROM BillingRecords")
                valid_billing_ids = cursor.fetchall()

                # Populate BillingDetails
                billing_details = []
                for billing_id, client_id in valid_billing_ids:
                    for waste_category_id in valid_waste_category_ids:
                        quantity_in_kg = 50  # Example: fixed quantity for simplicity
                        subtotal = quantity_in_kg * 0.5  # Assume some unit price
                        billing_details.append(
                            (billing_id, waste_category_id, quantity_in_kg, round(subtotal, 2)))

                cursor.executemany("""
                    INSERT INTO BillingDetails (BillingID, WasteCategoryID, QuantityInKg, SubTotal)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, billing_details)
                conn.commit()

                print("Database populated successfully!")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    populate_database()
