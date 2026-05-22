import hashlib
from db import create_connection

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role):

    connection = create_connection()

    cursor = connection.cursor()

    hashed_password = hash_password(password)

    query = """
    INSERT INTO users
    (username, hashed_password, role)
    VALUES (%s, %s, %s)
    """

    values = (username, hashed_password, role)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

def login_user(username, password):

    connection = create_connection()

    cursor = connection.cursor()

    hashed_password = hash_password(password)

    query = """
    SELECT * FROM users
    WHERE username=%s
    AND hashed_password=%s
    """

    cursor.execute(query, (username, hashed_password))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user