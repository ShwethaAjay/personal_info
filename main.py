from __future__ import annotations
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel


#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

class Info(BaseModel):
    name: str
    email: str
    aadhar: str
    mobile: str


app = FastAPI()

@app.post("/personalinfo")
async def personal_info(item: Info):
    insert_data(item.email, item.name, item.aadhar, item.mobile)



# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('personal_info.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store the information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS personal_info (
        email VARCHAR PRIMARY KEY,
        name VARCHAR,
        aadhar TEXT,
        mobile TEXT
    )
''')

# Function to insert data into the database
def insert_data(email, name, aadhar, mobile):
    cursor.execute('''
        INSERT INTO personal_info (email, name, aadhar, mobile)
        VALUES (?, ?, ?, ?)
    ''', (email, name, aadhar, mobile))
    conn.commit()

# Function to retrieve data from the database
# def fetch_data():
#     cursor.execute('''
#         SELECT * FROM personal_info
#     ''')
#     return cursor.fetchall()


def databs():
    # Example usage
    insert_data('johnd@gmail.com','John Doe', '1234567890', '1234 5678 9012')
    insert_data('janes@gmail.com','Jane Smith', '9876543210', '9876 5432 1098')

    # Close the cursor and connection
    cursor.close()

