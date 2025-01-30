import mysql.connector
import pandas as pd

# Load the CSV file
file_path = r"C:\Users\sanke\Downloads\laptop_data.csv"
data = pd.read_csv(file_path)

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="admin"
)

cursor = mydb.cursor()

# Create the table 'laptopdata'
create_table_query = """
CREATE TABLE IF NOT EXISTS laptopdata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Company VARCHAR(255),
    TypeName VARCHAR(255),
    Inches FLOAT,
    ScreenResolution VARCHAR(255),
    Cpu VARCHAR(255),
    Ram VARCHAR(50),
    Memory VARCHAR(255),
    Gpu VARCHAR(255),
    OpSys VARCHAR(255),
    Weight VARCHAR(50),
    Price FLOAT
);
"""

cursor.execute(create_table_query)

# Insert data into the table
insert_query = """
INSERT INTO laptopdata (Company, TypeName, Inches, ScreenResolution, Cpu, Ram, Memory, Gpu, OpSys, Weight, Price)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in data.iterrows():
    cursor.execute(insert_query, (
        row['Company'],
        row['TypeName'],
        row['Inches'],
        row['ScreenResolution'],
        row['Cpu'],
        row['Ram'],
        row['Memory'],
        row['Gpu'],
        row['OpSys'],
        row['Weight'],
        row['Price']
    ))

# Commit the transaction and close the connection
mydb.commit()
cursor.close()
mydb.close()

print("Data uploaded successfully!")
