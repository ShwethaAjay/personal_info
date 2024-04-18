from __future__ import annotations
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status

app = FastAPI()

aadharlist = ["1234 5678 9012", "1234 5678 9013", "1235 4587 9102"]

@app.get("/verify/{aadhar}")
async def verify(aadhar):
     if aadhar in aadharlist :
         return status.HTTP_200_OK
     else:
         return status.HTTP_401_UNAUTHORIZED