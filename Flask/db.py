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

def get_user_data(user):
    database = connect()
    cursor = database.cursor(dictionary=True)

    query = "SELECT username, password, email, city, street, apartment_num, phone FROM `lokal-kebab`.Users WHERE username = %s"
    cursor.execute(query, (user,))

    result = cursor.fetchone()
    result = json.dumps(result)

    cursor.close()
    database.close()
    return result

def change_user_data(column, data, user):
    database = connect()
    cursor = database.cursor()

    if column == "email":
        query = "UPDATE `lokal-kebab`.Users SET email = %s WHERE username = %s"
    elif column == "password":
        query = "UPDATE `lokal-kebab`.Users SET password = %s WHERE username = %s"        
    elif column == "city":
        query = "UPDATE `lokal-kebab`.Users SET city = %s WHERE username = %s"
    elif column == "street":
        query = "UPDATE `lokal-kebab`.Users SET street = %s WHERE username = %s"
    elif column == "apartment_num":
        query = "UPDATE `lokal-kebab`.Users SET apartment_num = %s WHERE username = %s"
    elif column == "phone":
        query = "UPDATE `lokal-kebab`.Users SET phone = %s WHERE username = %s"

    cursor.execute(query, (data, user))
    database.commit()

    cursor.close()
    database.close()

def check_username(username):
    database = connect()
    cursor = database.cursor()

    query = "SELECT username FROM `lokal-kebab`.Users WHERE username = %s" 
    cursor.execute(query, (username,))

    result = cursor.fetchone()

    cursor.close()
    database.close()
    return result

def create_user(username, password, email, phone):
    database = connect()
    cursor = database.cursor()

    query = "INSERT INTO `lokal-kebab`.Users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (username, password, email, phone)) 
    database.commit()

    cursor.close()
    database.close()

    return 'success'