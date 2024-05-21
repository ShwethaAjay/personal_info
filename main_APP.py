from __future__ import annotations
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
import json
from requests import post


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


def pkcs10enroll(csr, caHost, trustChainFile, clientCrt, clientKey, certProfile, eeProfile, caName):
    
    print(csr)
    
    postURL = 'https://' + caHost + '/ejbca/ejbca-rest-api/v1/certificate/pkcs10enroll'
    
    response = post(postURL,
        json={
          "certificate_request": csr,
          "certificate_profile_name": certProfile,
          "end_entity_profile_name": eeProfile,
          "certificate_authority_name": caName,
        },
        headers={
            'content-type': 'application/json'
        },
        verify=False,
        cert=(clientCrt, clientKey))
     
    print (response.content)
    print(json.dumps(json.loads(response.content), indent=4, sort_keys=True))
     
    json_resp = response.json()
     
    cert = json_resp['certificate']
     
    #reconstruct certificate from json array
    pem = "-----BEGIN CERTIFICATE-----"
    for i in range(len(cert)):
        if i % 64 == 0:
            pem += "\n"
        pem += cert[i]
     
    pem += "\n-----END CERTIFICATE-----"

    output_cert = json_resp['serial_number'] + ".pem"
    out_file = open(output_cert, "w")
    out_file.write(pem)
    out_file.close()
     
    return pem

class cert_req(BaseModel):
    csr : str | None = None

@app.post("/csr")
def csr_approve(csr : cert_req):
    print(csr)
    cert = pkcs10enroll(csr.csr , "192.168.93.193" , "ManagementCA.cacert.pem" , "SuperAdmin.pem" , "SuperAdmin.key" , "MIDEND" , "MIDEND" , "ManagementCA")
    return {"certificate" : cert}