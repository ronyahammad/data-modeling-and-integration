import psycopg2
import mysql.connector

import csv

def fetch_mysql_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password='root',
            database='WaterManagement'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                
                with open(f"water_mysql_{table_name.lower()}.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)
                    writer.writerows(rows)

            print("MySQL data extraction complete.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            connection.close()


def main():
    fetch_mysql_data()


if __name__ == "__main__":
    main()
