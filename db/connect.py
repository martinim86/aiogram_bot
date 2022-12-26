from mysql.connector import connect, Error
import mysql.connector
DB_HOST = 'localhost'
DB_USER = 'summy'
DATABASE_NAME = 'bot'
DB_PASSWORD = 'summy'
DB_PORT = '3306'
TEST_DATABASE_NAME = 'mydb'

mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DATABASE_NAME
)
mycursor = mydb.cursor()