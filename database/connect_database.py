import bcrypt
import json
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
# from features.Profile import view_user

cloud_config = {
    'secure_connect_bundle': 'database/secure-connect-eduflex.zip'
}

with open("database/sarampentapraveen@gmail.com-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)

execution_profile = ExecutionProfile(
    load_balancing_policy=DCAwareRoundRobinPolicy()
)

cluster = Cluster(
    cloud=cloud_config,
    auth_provider=auth_provider,
    connect_timeout=60,
    execution_profiles={EXEC_PROFILE_DEFAULT: execution_profile}
)

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
    create_logs_table = """
    CREATE TABLE IF NOT EXISTS logs (
        user_email TEXT,
        log_date DATE,
        log_time TIMESTAMP,
        log_level TEXT,
        message TEXT,
        PRIMARY KEY (user_email, log_date, log_time)
    )
    """
    try:
        session.execute(create_register_table)
        print("Table 'register' created successfully!")

        session.execute(create_logs_table)
        print("Table 'logs' created successfully!")
    except Exception as e:
        print(f"Failed to create 'register' table. Error: {e}")


def register_account(fname, lname, email, password, ids):
    name = f"{fname} {lname}"
    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    try:
        session.execute(
            "INSERT INTO register (id, name, email, password) VALUES (%s, %s, %s, %s)",
            (ids, name, email, hashed_password)
        )
        print("Account registered successfully!")
        # view_user(dict({'first_name': fname,'last_name': lname,'email': email,'password': password}))
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
            "SELECT id FROM register WHERE email = %s ALLOW FILTERING", (email,))
        if result:
            return result[0].id
        else:
            return None
    except Exception as e:
        print(f"Failed to get id by email. Error: {e}")
        return None

def insert_log(user_email, log_level, message):
    if not user_email or user_email.strip() == "":
        print("Error: User email cannot be empty!")
        return False

    try:
        session.execute("""
            INSERT INTO logs (user_email, log_date, log_time, log_level, message)
            VALUES (%s, toDate(now()), toTimestamp(now()), %s, %s)
        """, (user_email, log_level, message))

        print("Log inserted successfully!")
        return True
    except Exception as e:
        print(f"Failed to add log. Error: {e}")
        return False



def fetch_logs(session, email=None):
    if email:
        query = "SELECT * FROM logs WHERE user_email=%s ORDER BY log_date DESC, log_time DESC"
        rows = session.execute(query, (email,))
    else:
        query = "SELECT * FROM logs ORDER BY log_date DESC, log_time DESC"
        rows = session.execute(query)

    for row in rows:
        print(row)
    return rows




def fetch_user_data(email):
    query = "SELECT id, name, email, password FROM register WHERE email = %s ALLOW FILTERING"
    result = session.execute(query, [email]).one()
    
    password = result.password
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    print(password)
    if result:
        name_parts = result.name.split(" ", 1)
        return {
            'first_name': name_parts[0] if len(name_parts) > 0 else "",
            'last_name': name_parts[1] if len(name_parts) > 1 else "",
            'email': result.email,
            'password': password
        }
    else:
        return None


def update_user_data(user_id, updated_data):
    """Update user details in Cassandra"""

    # Combine first and last name into one
    full_name = f"{updated_data.get('first_name', '')} {updated_data.get('last_name', '')}".strip()

    if 'password' in updated_data:
        hashed_password = bcrypt.hashpw(updated_data['password'].encode(), bcrypt.gensalt()).decode('utf-8')
        print("Password encrypted...")
        query = """
        UPDATE register 
        SET name = %s, password = %s 
        WHERE id = %s
        """
        session.execute(query, [full_name, hashed_password, user_id])
        print("Password change:", updated_data)
    else:
        query = """
        UPDATE register 
        SET name = %s 
        WHERE id = %s
        """
        session.execute(query, [full_name, user_id])
        print("Name change:", updated_data)

    print("User details updated successfully!")


if __name__ == '__main__':
    # Create the 'register' table
    # create_tables()
    # print("Created table...")
    # session.execute("TRUNCATE TABLE register")
    # session.execute("DROP TABLE IF EXISTS logs;")
    # print("dropped...")

    rows = session.execute("SELECT * FROM register")
    for row in rows:
        print(row)
    # session.execute("TRUNCATE TABLE register")
    
    #  # Test data
    # fname = "John"
    # lname = "Doe"
    # email = "johndoe@example.com"
    # password = "password123"
    # ids = 1

    # # Test registration
    # print("\n--- Register Account Test ---")
    # register_account(fname, lname, email, password, ids)
    # user_id = get_id_by_email(email)
    # if user_id:
    #     print(f"Registration successful! User ID: {user_id}")
    # else:
    #     print("Registration failed!")

    # # Test successful login
    # print("\n--- Login Test (Success) ---")
    # login_result = login(email, password)
    # if login_result:
    #     print("Login successful!")
    # else:
    #     print("Login failed!")

    # # Test login with incorrect password
    # print("\n--- Login Test (Failure: Wrong Password) ---")
    # wrong_password_result = login(email, "wrongpassword")
    # if not wrong_password_result:
    #     print("Login failed with incorrect password (expected).")
    # else:
    #     print("Login succeeded unexpectedly with incorrect password!")

    # # Test login with non-existent user
    # print("\n--- Login Test (Failure: Non-existent User) ---")
    # non_existent_user_result = login("nonexistent@example.com", password)
    # if not non_existent_user_result:
    #     print("Login failed for non-existent user (expected).")
    # else:
    #     print("Login succeeded unexpectedly for non-existent user!")

    # # Test fetching user details
    # print("\n--- Fetch User Details ---")
    user_name = get_name("sarampentapraveen@gmail.com")
    if user_name:
        print(f"Fetched user name: {user_name}")
    else:
        print("Failed to fetch user name!")

    # # Print all records in the table
    # print("\n--- All Records in 'register' Table ---")
    # rows = session.execute("SELECT * FROM register")
    # for row in rows:
    #     print(row)


    # user_id = "praveen@gmail.com"
    # user_data = fetch_user_data(session, user_id)

    # print(user_data)

    default_user = {
        'first_name': "Praveen",
        'last_name': "Chary",
        'email': "sarampentapraveen@gmail.com",
        'password': "1234"
    }
    ids = get_id_by_email("sarampentapraveen@gmail.com")

    update_user_data(ids, default_user)

    


