import mysql.connector

username = "' OR 'a'='a';--"
password = " "

connection = mysql.connector.connect(
    host="localhost",
    database="oop_project")
cursor = connection.cursor()
cursor.execute("SELECT * FROM manager WHERE adminId = '%s' AND adminPassword = '%s'" % (username, password))

record = cursor.fetchall()
if record:
    print(record)
else:
    print("record not found")

# disconnect from server
cursor.close()
connection.close()
