import mysql.connector
from mysql.connector import errorcode
# import textwrap
import hashlib

def init_db_connection():
    try:
        mydb = mysql.connector.connect(
            host="todo-mysql.default.svc.cluster.local",
            # host="localhost",
            user="root",
            password="octoberfest",
            database="todo_db"
        )
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    else:
        return mydb

def init_tables():
    cnx = init_db_connection()
    #Creating a cursor object using the cursor() method
    mycursor = cnx.cursor()

    sql_string = '''
CREATE DATABASE IF NOT EXISTS todo_db;

CREATE TABLE IF NOT EXISTS driver (
    email_id VARCHAR (255) PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    pwd TEXT,
    mobile TEXT,
    onb_status TEXT,
    onb_comment TEXT,
    is_available BOOLEAN,
    plate_number TEXT,
    vehicle TEXT
);

CREATE TABLE IF NOT EXISTS approval (
    email_id VARCHAR (255) PRIMARY KEY,
    status TEXT,
    comment TEXT,
    action_by TEXT
);
'''
    try:
        mycursor.execute(sql_string)
        mycursor.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    else:
        print("tables intialised successfully")
        
def check_if_row_exists(email_id: str):
    cnx = init_db_connection()
    mycursor = cnx.cursor()
    try:
        mycursor.execute('SELECT EXISTS(SELECT * FROM driver WHERE email_id=%s)', [email_id])
        myresult = mycursor.fetchall()
        mycursor.close()
        print(myresult)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    cnx.close()

def fetch_driver_row(email_id: str):
    cnx = init_db_connection()

    try:
        mycursor = cnx.cursor()
        mycursor.execute('SELECT * FROM driver WHERE email_id=%s', [email_id])
        myresult = mycursor.fetchall()
        mycursor.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    cnx.close()
    return myresult[0] if myresult else None

def insert_driver_row(row_data):
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "INSERT INTO driver (email_id, first_name, last_name, mobile, pwd, onb_status, onb_comment, is_available, plate_number, vehicle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql_query, 
                     [row_data["email_id"],
                     row_data["first_name"],
                     row_data["last_name"],
                     row_data["mobile"],
                     hashlib.sha512(row_data["pwd"].encode('UTF-8')).hexdigest(),
                     row_data["onb_status"],
                     row_data["onb_comment"],
                     row_data["is_available"],
                     row_data["plate_number"],
                     row_data["vehicle"]],
                     )
    mycursor.close()
    cnx.commit()
    print(mycursor.rowcount, "record inserted")

def update_driver_row(row_data):
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "UPDATE driver SET onb_status=%s, onb_comment=%s WHERE email_id=%s"
    mycursor.execute(sql_query, 
                     [row_data["status"],
                     row_data["comment"],
                     row_data["email_id"]],
                     )
    mycursor.close()
    cnx.commit()
    print(mycursor.rowcount, "record updated in driver table")


def update_driver_availability(row_data):
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "UPDATE driver SET is_available=%s WHERE email_id=%s"
    mycursor.execute(sql_query, 
                     [row_data["is_available"],
                     row_data["email_id"]]
                     )
    mycursor.close()
    cnx.commit()
    print(mycursor.rowcount, "record updated in driver table")

def insert_approval_row(row_data):
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "INSERT INTO approval (email_id, status, comment, action_by) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql_query, 
                     [row_data["email_id"],
                     row_data["status"],
                     row_data["comment"],
                     row_data["action_by"]]
                     )
    mycursor.close()
    cnx.commit()
    print(mycursor.rowcount, "record inserted")


def update_approval_row(row_data):
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "UPDATE approval SET status=%s, comment=%s, action_by=%s WHERE email_id=%s;"
    mycursor.execute(sql_query, 
                     [row_data["status"],
                     row_data["comment"],
                     row_data["action_by"],
                     row_data["email_id"]]
                     )
    mycursor.close()
    cnx.commit()
    print(mycursor.rowcount, "record updated in approval table")

def list_all_approvals():
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "SELECT * FROM approval ;"
    mycursor.execute(sql_query)
    myresult = mycursor.fetchall()
    mycursor.close()
    print(mycursor.rowcount, "record updated in approval table")

    return myresult

def fetch_drivers():
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "SELECT * FROM driver;"
    mycursor.execute(sql_query)
    myresult = mycursor.fetchall()
    print(mycursor.rowcount, "records fetched from driver table")
    mycursor.close()

    return myresult

def fetch_driver_info(email_id):
    cnx = init_db_connection()

    mycursor = cnx.cursor()
    sql_query = "SELECT * FROM driver WHERE email_id=%s;"
    mycursor.execute(sql_query, [email_id])
    myresult = mycursor.fetchall()
    print(mycursor.rowcount, "records fetched from driver table")
    mycursor.close()

    return myresult