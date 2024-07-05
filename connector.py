import mysql.connector
from mysql.connector import Error
import setting as sett 

def connect_database():
    conn = mysql.connector.connect(
        host=sett.DB_HOST,
        user=sett.DB_USER,
        password=sett.DB_PASSWORD,
        database=sett.DB_NAME
    )
    return conn

def disconnect_database(conn):
    conn.close()