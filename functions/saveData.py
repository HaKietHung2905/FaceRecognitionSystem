import mysql.connector  
import argparse
import os

import configparser

def read_config(database_name):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[database_name]

# Function to fetch store data from SQL Server
def connect_database(name):
    config_data = read_config(name)

    host = config_data['server']
    database = config_data['database']
    username = config_data['username']
    password = config_data['password']

    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database= database
    )
    
    cursor = db_connection.cursor()

    # Define your SELECT query
    query = "SELECT * FROM testtable"

    # Execute the query
    cursor.execute(query)

    # Fetch all the rows
    records = cursor.fetchall()

    # Display the records
    for record in records:
        print(record)
#
#    for filename, query in queries.items():
#        try:
#            cursor.execute(query)
#            results = cursor.fetchall()
#            result_string = ''.join([str(row.definition) for row in results])
            #print(result_string)
#            result_data.append({'filename': filename, 'data': result_string})
#        except Exception as e:
            # Handle exceptions (customize as needed)
#            print(f"Error executing query for {filename}: {e}")

#    connection.close()
#    return result_data

if __name__ == "__main__":
    connect_database('database')