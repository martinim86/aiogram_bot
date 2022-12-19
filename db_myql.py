from mysql.connector import connect, Error
import mysql.connector
import csv
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

def select_user(firstname):
    list = []
    dir = list.append(firstname)
    sql = "SELECT name FROM customers WHERE name = %s"

    mycursor.execute(sql,list)
    myresult = mycursor.fetchone()
    return myresult
def create_user(firstname, balance):
    sql = "INSERT INTO customers (name, balance) VALUES (%s, %s)"
    val = (firstname, balance)
    mycursor.execute(sql, val)

    mydb.commit()
def select_users():
    mycursor.execute("SELECT * FROM customers")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
def delete_user():
    sql = "DELETE FROM customers WHERE name = 'Ivan'"

    mycursor.execute(sql)

    mydb.commit()
def update_users(firstname, balance):
    sql = "SELECT balance FROM customers WHERE name =  %s"
    list = []
    dir = list.append(firstname)
    mycursor.execute(sql, list)
    myresult = mycursor.fetchone()
    for x in myresult:
        i = int(x)+int(balance)
    sql = "UPDATE customers SET balance = %s  WHERE name = %s"

    val = (i, firstname)
    mycursor.execute(sql, val)
    mydb.commit()


def block_user(firstname):
    list = []
    dir = list.append(firstname)
    sql = "UPDATE customers SET block =1 WHERE name = %s"
    mycursor.execute(sql, list)
    mydb.commit()
def export_file():
    mycursor.execute("SELECT * FROM customers")

    myresult = mycursor.fetchall()
    fp = open('file.csv', 'w')
    myFile = csv.writer(fp)
    myFile.writerows(myresult)
    fp.close()
def insert_payment(p_name, p_pay,p_date):
    sql = "INSERT INTO payments (p_name, p_pay,p_date ) VALUES (%s, %s, %s)"
    val = (p_name, p_pay,p_date)
    mycursor.execute(sql, val)
    mydb.commit()
def select_pay():
    mycursor.execute("SELECT * FROM payments")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


