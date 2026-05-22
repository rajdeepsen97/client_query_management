import mysql.connector

def create_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="January@2026",
        database="client_query_system"
    )

    return connection