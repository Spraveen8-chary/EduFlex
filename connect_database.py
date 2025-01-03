import bcrypt
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
import json
import streamlit as st
cloud_config = {
    'secure_connect_bundle': r'D:\EDUFLEX\secure-connect-eduflex.zip'
}

with open("theja2k26@gmail.com-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider,connect_timeout=60,load_balancing_policy=DCAwareRoundRobinPolicy())
session = cluster.connect()

keyspace_name = 'database'

session.execute(f"USE {keyspace_name}")


def create_tables():

    create_register_table = """
    CREATE TABLE IF NOT EXISTS register (
        id INT PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """
    try:
        session.execute(create_register_table)
        print("Table 'register' created successfully!")
    except Exception as e:
        print(f"Failed to create 'register' table. Error: {e}")


def register_account(fname, lname, email, password, ids):
    name = f"{fname} {lname}"
    
    # Generate bcrypt password hash
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    try:
        session.execute(
            "INSERT INTO register (id, name, email, password) VALUES (%s, %s, %s, %s)",
            (ids, name, email, hashed_password)
        )
        print("Account registered successfully!")
        return True
    except Exception as e:
        print(f"Failed to register account. Error: {e}")
        return False


def login(email, password):
    result = session.execute(
        "SELECT email, password FROM register WHERE email = %s ALLOW FILTERING",
        (email,)
    )
    for row in result:
        # Check if the bcrypt hash matches the password
        if bcrypt.checkpw(password.encode(), row.password.encode()):
            return True
    return False


def get_name(email):
    result = session.execute("SELECT name, email FROM register WHERE email = %s ALLOW FILTERING", (email,))
    if not result:
        return None

    for row in result:
        return row.name


def get_id_by_email(email):
    try:
        result = session.execute(
            "SELECT id FROM register WHERE email = %s LIMIT 1", (email,))
        if result:
            return result[0].id
        else:
            return None
    except Exception as e:
        print(f"Failed to get id by email. Error: {e}")
        return None


if __name__ == '__main__':
    # Create the 'register' table
    # create_tables()
    # print("Created table...")
    session.execute("TRUNCATE TABLE register")

    rows = session.execute("SELECT * FROM register")
    for row in rows:
        print(row)
    session.execute("TRUNCATE TABLE register")
    
     # Test data
    fname = "John"
    lname = "Doe"
    email = "johndoe@example.com"
    password = "password123"
    ids = 1

    # Test registration
    print("\n--- Register Account Test ---")
    register_account(fname, lname, email, password, ids)
    user_id = get_id_by_email(email)
    if user_id:
        print(f"Registration successful! User ID: {user_id}")
    else:
        print("Registration failed!")

    # Test successful login
    print("\n--- Login Test (Success) ---")
    login_result = login(email, password)
    if login_result:
        print("Login successful!")
    else:
        print("Login failed!")

    # Test login with incorrect password
    print("\n--- Login Test (Failure: Wrong Password) ---")
    wrong_password_result = login(email, "wrongpassword")
    if not wrong_password_result:
        print("Login failed with incorrect password (expected).")
    else:
        print("Login succeeded unexpectedly with incorrect password!")

    # Test login with non-existent user
    print("\n--- Login Test (Failure: Non-existent User) ---")
    non_existent_user_result = login("nonexistent@example.com", password)
    if not non_existent_user_result:
        print("Login failed for non-existent user (expected).")
    else:
        print("Login succeeded unexpectedly for non-existent user!")

    # Test fetching user details
    print("\n--- Fetch User Details ---")
    user_name = get_name(email)
    if user_name:
        print(f"Fetched user name: {user_name}")
    else:
        print("Failed to fetch user name!")

    # Print all records in the table
    print("\n--- All Records in 'register' Table ---")
    rows = session.execute("SELECT * FROM register")
    for row in rows:
        print(row)