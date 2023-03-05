import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        return connection
    except (Error, ConnectionError, AttributeError):
        return 'NotConn'

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except (Error, AttributeError):
        pass

def execute_read_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except (Error, ConnectionError, AttributeError):
        return 'NotConn'
