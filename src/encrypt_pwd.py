import mysql.connector
import bcrypt

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    database="final_project"
)
cursor = db_connection.cursor()

# User login
def authenticate_user(username, passphrase):
    cursor.execute("SELECT User_Pwd, salt FROM keystroke WHERE User_ID = %s", (username,))
    result = cursor.fetchone()
    if result:
        hashed_password, salt = result
        salt = salt.encode('utf-8')
        stored_hashed_password = hashed_password.encode('utf-8')
        input_hashed_password = bcrypt.hashpw(passphrase.encode('utf-8'), salt)
        print(salt)
        print(input_hashed_password)
        print(stored_hashed_password)
        if input_hashed_password == stored_hashed_password:
            return True
    return False

# Test registration and authentication
username = "Z1"
password = "call me by your name"

if authenticate_user(username, password):
    print("Authentication successful.")
else:
    print("Authentication failed.")
