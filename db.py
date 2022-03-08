import mysql.connector

def connector():


    connection = mysql.connector.connect(host='localhost', user='root',password='', database='test')
    return connection
