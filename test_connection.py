from db import create_connection

connection = create_connection()

if connection.is_connected():
    print("MySQL Connected Successfully!")
else:
    print("Connection Failed")