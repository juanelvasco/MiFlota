import mysql.connector

database = mysql.connector.connect(
    user='root', password='juanelvasco1',
    host='127.0.0.1', port='3306',
    database='flotaDB'
)