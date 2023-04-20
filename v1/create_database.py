import mysql.connector

# Connect to MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vep4pta8xv@"
)

# Create a cursor object to execute SQL statements
cursor = db.cursor()

# Execute SQL query to create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS world")

# Close cursor and database connections
cursor.close()
db.close()

# Connect to MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vep4pta8xv@",
    database="world"
)

# Create a cursor object to execute SQL statements
cursor = db.cursor()

# Create studentInfo table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS studentInfo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        password VARCHAR(255) CHECK(length(password) >= 8),
        gender VARCHAR(10),
        phonenumber VARCHAR(20),
        email VARCHAR(255),
        birth_year INT
    )
""")

# Create staffInfo table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS staffInfo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        password VARCHAR(255) CHECK(length(password) >= 8),
        gender VARCHAR(10),
        phonenumber VARCHAR(20),
        email VARCHAR(255),
        birth_year INT
    )
""")

# Create adminInfo table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS adminInfo (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) CHECK(length(password) >= 8)
    )
""")

# Create notice table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS notice (
        id INT PRIMARY KEY AUTO_INCREMENT,
        announcement TEXT
    )
""")

# Create attendance table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT PRIMARY KEY AUTO_INCREMENT,
        date DATE,
        student_name VARCHAR(255),
        subject VARCHAR(255),
        attendance VARCHAR(255) DEFAULT 'N'
    )
""")

# Create grades table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INT PRIMARY KEY AUTO_INCREMENT,
        student_name VARCHAR(255),
        subject VARCHAR(255),
        grade VARCHAR(255),
        date DATE
    )
""")

    # Create the new table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recent_users (
            username VARCHAR(255)
        )
    """)

# Close cursor and database connections
cursor.close()
db.close()
