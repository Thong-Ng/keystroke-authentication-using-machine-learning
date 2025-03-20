import mysql.connector

# Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    database="final_project"
)

# Create a cursor
cursor = connection.cursor()

# Example data
new_data = {
    "User_ID": "John",
    "User_Pwd": "john@example.com",
    "key_1": 116.9639,
    "key_2": 171.1068,
    "key_3": 85.2289,
    "key_4": 273.0472,
    "key_5": 137.3239
}

# Insert data into the table
insert_query = "INSERT INTO user (User_ID, User_Pwd, key_1, key_2, key_3, key_4, key_5) VALUES (%s, %s, %s, %s, %s, %s, %s)"
data_values = (new_data["User_ID"], new_data["User_Pwd"], new_data["key_1"], new_data["key_2"], new_data["key_3"], new_data["key_4"], new_data["key_5"])
cursor.execute(insert_query, data_values)

# Commit the transaction
connection.commit()

cursor.close()
connection.close()
