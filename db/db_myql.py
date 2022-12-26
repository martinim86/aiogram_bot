from db.connect import mycursor, mydb
import csv

class Database:
    def select_user(self, firstname):
        list = []
        dir = list.append(firstname)
        sql = "SELECT name FROM customers WHERE name = %s"

        mycursor.execute(sql, list)
        myresult = mycursor.fetchone()
        return myresult

    def create_user(self, firstname, balance):
        sql = "INSERT INTO customers (name, balance) VALUES (%s, %s)"
        val = (firstname, balance)
        mycursor.execute(sql, val)

        mydb.commit()

    def select_users(self):
        mycursor.execute("SELECT * FROM customers")

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)

    def delete_user(self):
        sql = "DELETE FROM customers WHERE name = 'Ivan'"

        mycursor.execute(sql)

        mydb.commit()

    def update_users(self, firstname, balance):
        sql = "SELECT balance FROM customers WHERE name =  %s"
        list = []
        dir = list.append(firstname)
        mycursor.execute(sql, list)
        myresult = mycursor.fetchone()
        for x in myresult:
            i = int(x) + int(balance)
        sql = "UPDATE customers SET balance = %s  WHERE name = %s"

        val = (i, firstname)
        mycursor.execute(sql, val)
        mydb.commit()

    def block_user(self, firstname):
        list = []
        dir = list.append(firstname)
        sql = "UPDATE customers SET block =1 WHERE name = %s"
        mycursor.execute(sql, list)
        mydb.commit()

    def export_file(self):
        mycursor.execute("SELECT * FROM customers")
        myresult = mycursor.fetchall()
        fp = open('sfile.csv', 'w')
        myFile = csv.writer(fp)
        myFile.writerows(myresult)
        fp.close()

    def insert_payment(self, p_name, p_pay, p_date):
        sql = "INSERT INTO payments (p_name, p_pay,p_date ) VALUES (%s, %s, %s)"
        val = (p_name, p_pay, p_date)
        mycursor.execute(sql, val)
        mydb.commit()

    def select_pay(self):
        mycursor.execute("SELECT * FROM payments")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
a = Database()
a.select_users()