import datetime
import os
import psycopg2
from psycopg2 import Error

# use python to get current time
def utc_timestamp():
    return datetime.datetime.utcnow()

def config():
    return [os.environ.get("POSTGRES_USER"),
        os.environ.get("POSTGRES_PASSWORD"),
        os.environ.get("POSTGRES_DB_HOST"),
        os.environ.get("POSTGRES_DB_PORT"),
        os.environ.get("POSTGRES_DB")]

conf = config()

def create_table_osm():
    try:
        connection = psycopg2.connect(user=conf[0],
                                    password=conf[1],
                                    host=conf[2],
                                    port=conf[3],
                                    database=conf[4])

        cursor = connection.cursor()
        # SQL query to create a new table
        create_table_query = '''CREATE TABLE osm_output_files
            (ID SERIAL PRIMARY KEY,
            FILE TEXT NOT NULL,
            DATA BYTEA NOT NULL,
            TIMESTAMP timestamp with time zone
            ); '''
        # Execute a command: this creates a new table
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def insert_data_osm(filename, data):
    try:
        connection = psycopg2.connect(user=conf[0],
                                    password=conf[1],
                                    host=conf[2],
                                    port=conf[3],
                                    database=conf[4])

        cursor = connection.cursor()
        # Insert data into table
        insert_query = """INSERT INTO osm_output_files (FILE, DATA, TIMESTAMP) VALUES (%s,%s,%s)"""
        record_to_insert = (filename, data, utc_timestamp())
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into osm_output_files table")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def select_data_osm():
    try:
        connection = psycopg2.connect(user=conf[0],
                                    password=conf[1],
                                    host=conf[2],
                                    port=conf[3],
                                    database=conf[4])

        cursor = connection.cursor()
        # Select data from table
        select_query = """select * from osm_output_files"""
        cursor.execute(select_query)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record selected successfully from osm_output_files table")
        print(cursor.fetchall())

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def delete_data_osm():
    try:
        connection = psycopg2.connect(user=conf[0],
                                    password=conf[1],
                                    host=conf[2],
                                    port=conf[3],
                                    database=conf[4])

        cursor = connection.cursor()
        # Delete data from table
        delete_query = """DELETE from osm_output_files where ID = %s"""
        cursor.execute(delete_query, (1,))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully from osm_output_files table")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def check_table_exists(table_name):
    try:
        connection = psycopg2.connect(user=conf[0],
                                    password=conf[1],
                                    host=conf[2],
                                    port=conf[3],
                                    database=conf[4])

        cursor = connection.cursor()
        # Check if table exists
        cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", (table_name,))
        exists = cursor.fetchone()[0]
        if exists:
            print("Table exists")
        else:
            print("Table does not exist")
            create_table_osm()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def save_file_to_db(table_name, file_name):
    in_file = open(file_name, "rb")
    data = in_file.read()
    in_file.close()

    if check_table_exists(table_name):
        insert_data_osm()
    else:
        create_table_osm()
        insert_data_osm(file_name, data)
