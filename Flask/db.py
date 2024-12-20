import mysql.connector
import json

def connect():
    database = mysql.connector.connect(
        host="jakubplewa.pl",
        user="jakub",
        password="jakub",
        port=3606
    )
    return database


def get_user(username, password):
    database = connect()
    cursor = database.cursor()

    # Zapytanie do bazy danych
    query = "SELECT password FROM `lokal-kebab`.Users WHERE username = %s AND password = %s" 
    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    cursor.close()
    database.close()
    return result

def get_menu():
    database = connect()
    cursor = database.cursor(dictionary=True)
    # Zapytanie do bazy danych
    query = "SELECT name, price, description, img_url FROM `lokal-kebab`.Menu" 
    cursor.execute(query)

    result = cursor.fetchall()
    result = json.dumps(result)

    cursor.close()
    database.close()
    return result
