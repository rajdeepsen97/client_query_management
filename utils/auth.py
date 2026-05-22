import bcrypt
from db import create_connection

def hash_password(password):
    """Hash a password using bcrypt with auto-generated salt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def verify_password(password, hashed_password):
    """Check a plain password against the stored bcrypt hash."""
    return bcrypt.checkpw(password.encode(), hashed_password)

def register_user(username, password, role):
    """Register a new user with a bcrypt hashed password."""
    connection = create_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    query = """
    INSERT INTO users (username, hashed_password, role)
    VALUES (%s, %s, %s)
    """
    values = (username, hashed_password, role)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

def login_user(username, password):
    """Fetch user by username and verify password."""
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user and verify_password(password, user[2]):
        return user

    return None