from datetime import datetime, timedelta
from decimal import Decimal
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
    query = "SELECT * FROM `lokal-kebab`.Menu" 
    cursor.execute(query)

    result = cursor.fetchall()
    result = json.dumps(result)

    cursor.close()
    database.close()
    return result

def get_user_data(user):
    database = connect()
    cursor = database.cursor(dictionary=True)

    query = "SELECT user_id, username, password, email, city, street, apartment_num, phone FROM `lokal-kebab`.Users WHERE username = %s"
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

def make_order(username, items, city, street, apartment_num, phone):
    if username == None:
        username = create_guest(city, street, apartment_num, phone)
        if username == None:
            return 'failed'

    query = "UPDATE `lokal-kebab`.Users SET city=%s, street=%s, apartment_num=%s, phone=%s WHERE username=%s"
    cursor.execute(query, (city, street, apartment_num, phone, username))

    database = connect()
    cursor = database.cursor()

    query = "SELECT menu_id FROM `lokal-kebab`.Menu WHERE name = %s"
    menu_ids = []
    quantity = []

    for item in items:
        cursor.execute(query, (item["name"],))
        result = cursor.fetchone()  # Pobiera jeden wynik
        if result:  # Sprawdza, czy wynik istnieje
            menu_ids.append(result[0])  # Dodaje menu_id (pierwsza kolumna w wyniku zapytania)
            quantity.append(item["quantity"]) # dodaje ilość

    query = "SELECT user_id FROM `lokal-kebab`.Users WHERE username = %s"
    cursor.execute(query, (username,)) 
    user_id = cursor.fetchone()[0]

    start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "W trakcie"

    query = "INSERT INTO `lokal-kebab`.Orders (status, Users_user_id, startDate) VALUES (%s, %s, %s)"
    cursor.execute(query, (status, user_id, start_date)) 
    order_id = cursor.lastrowid

    query = "INSERT INTO `lokal-kebab`.Order_menu (order_id, menu_id, quantity) VALUES (%s, %s, %s)"
    for i in range(len(menu_ids)):
        cursor.execute(query, (order_id, menu_ids[i], quantity[i])) 

    database.commit()

    cursor.close()
    database.close()

    return 'success'

def create_guest(city, street, apartment_num, phone):
    try:
        start_date = datetime.now().strftime('%d%m%Y%H%M%S')
        username = "guest" + start_date
    
        database = connect()
        cursor = database.cursor()

        query = "INSERT INTO `lokal-kebab`.Users (username, city, street, apartment_num, phone, is_temp) VALUES (%s, %s, %s, %s, %s, 'YES')"
        cursor.execute(query, (username, city, street, apartment_num, phone))

        database.commit()

        cursor.close()
        database.close()

        return username
    except:
        print("Cannot create a guest account")
        return None
    
def get_users_data():
    database = connect()
    cursor = database.cursor(dictionary=True)

    query = "SELECT user_id ,username, password, email, city, street, apartment_num, phone FROM `lokal-kebab`.Users WHERE is_temp = 'NO' ORDER BY username ASC"
    cursor.execute(query)

    result = cursor.fetchall()
    result = json.dumps(result)

    cursor.close()
    database.close()
    return result   

def delete_user_from_db(username):
    database = connect()
    cursor = database.cursor()

    query = "SELECT user_id FROM `lokal-kebab`.Users WHERE username = %s"
    cursor.execute(query, (username,))

    user_id = cursor.fetchone()[0]
    
    query = "DELETE FROM `lokal-kebab`.Orders WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    query = "DELETE FROM `lokal-kebab`.Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    database.commit()
    cursor.close()
    database.close()

def change_menu(column, data, name):
    database = connect()
    cursor = database.cursor()

    query = "SELECT menu_id FROM `lokal-kebab`.Menu WHERE name = %s"
    cursor.execute(query, (name,))
    menu_id = cursor.fetchone()[0]

    if column == "name":
        query = "UPDATE `lokal-kebab`.Menu SET name = %s WHERE menu_id = %s"
    elif column == "price":
        query = "UPDATE `lokal-kebab`.Menu SET price = %s WHERE menu_id = %s"        
    elif column == "description":
        query = "UPDATE `lokal-kebab`.Menu SET description = %s WHERE menu_id = %s"
    elif column == "img_url":
        query = "UPDATE `lokal-kebab`.Menu SET img_url = %s WHERE menu_id = %s"

    cursor.execute(query, (data, menu_id))
    database.commit()

    cursor.close()
    database.close()

def get_position_from_menu(name):
    database = connect()
    cursor = database.cursor(dictionary=True)

    query = "SELECT * FROM `lokal-kebab`.Menu WHERE name = %s"
    cursor.execute(query, (name,))

    data = cursor.fetchone()
    data = json.dumps(data)
    cursor.close()
    database.close()
    return data

def delete_menu_from_db(name):
    database = connect()
    cursor = database.cursor()

    query = "DELETE FROM `lokal-kebab`.Menu WHERE name = %s"
    cursor.execute(query, (name,))

    database.commit()
    cursor.close()
    database.close()   

def create_menu(name, price, description, img_url):
    try:    
        database = connect()
        cursor = database.cursor()

        query = "INSERT INTO `lokal-kebab`.Menu (name, price, description, img_url) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, price, description, img_url))

        database.commit()

        cursor.close()
        database.close()

    except:
        print("Cannot create menu")
        cursor.close()
        database.close()

def get_orders():
    database = connect()
    cursor = database.cursor(dictionary=True)

    cursor.execute("USE `lokal-kebab`")

    status = "W trakcie"

    query ="""SELECT o.order_id, o.status, o.startDate, o.endDate, o.discount_value, u.username, GROUP_CONCAT( DISTINCT u.city, ' ul. ', u.street, '/', u.apartment_num) AS address, u.phone, GROUP_CONCAT(om.quantity, 'x ', m.name) AS items, SUM(m.price * om.quantity) AS total_price
            FROM Orders o
            JOIN Users u ON o.Users_user_id = u.user_id
            JOIN Order_menu om ON o.order_id = om.order_id
            JOIN Menu m ON om.menu_id = m.menu_id
            GROUP BY o.order_id, o.status, o.startDate, o.endDate, o.discount_value, u.username, u.city, u.street, u.apartment_num, u.phone
            HAVING o.status = %s
            ORDER BY o.startDate ASC; """
    cursor.execute(query, (status,))
    orders = cursor.fetchall()

    # Przetwarzanie wyników (zamiana timedelta na string oraz Decimal na float)
    for order in orders:
        for key, value in order.items():
            if isinstance(value, datetime): # Jeśli wartość to timedelta
                order[key] = str(value)      # Zamień na string w formacie "HH:MM:SS"
            if isinstance(value, Decimal):   # Jeśli wartość to Decimal
                order[key] = float(value)    # Zamień na float

    orders = json.dumps(orders)

    cursor.close()
    database.close()

    return orders

def change_status(status, order_id):
    database = connect()
    cursor = database.cursor()

    end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = "UPDATE `lokal-kebab`.Orders SET status = %s, endDate = %s WHERE order_id = %s"
    cursor.execute(query, (status, end_date, order_id))
    database.commit()

    if check_temp(order_id) == 'YES':
        delete_temp(order_id)

    cursor.close()
    database.close()

def check_temp(order_id):
    database = connect()
    cursor = database.cursor()  
    cursor.execute("USE `lokal-kebab`")

    query = "SELECT u.is_temp FROM Orders o JOIN Users u ON o.Users_user_id = u.user_id WHERE o.order_id  = %s"
    cursor.execute(query, (order_id,))
    temp = cursor.fetchone()[0]

    cursor.close()
    database.close()

    return temp

def delete_temp(order_id):
    database = connect()
    cursor = database.cursor() 
    cursor.execute("USE `lokal-kebab`") 

    query = "SELECT u.user_id FROM Users u JOIN Orders o ON u.user_id = o.Users_user_id WHERE o.order_id = %s"
    cursor.execute(query, (order_id,))
    user_id = cursor.fetchone()[0]

    # Usuwa z tablicy Orders
    query = "DELETE FROM Orders WHERE order_id = %s"
    cursor.execute(query, (order_id,))

    # Usuwa z tablicy Users
    query = "DELETE FROM Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    database.commit()

    cursor.close()
    database.close()

def get_order_history(username):
    database = connect()
    cursor = database.cursor(dictionary=True) 
    cursor.execute("USE `lokal-kebab`") 

    query = """SELECT o.status, o.startDate, o.endDate, GROUP_CONCAT(om.quantity, 'x ', m.name) AS items, SUM(m.price * om.quantity) AS total_price
            FROM Orders o
            JOIN Users u ON o.Users_user_id = u.user_id
            JOIN Order_menu om ON o.order_id = om.order_id
            JOIN Menu m ON om.menu_id = m.menu_id
            WHERE username = %s
            GROUP BY o.status, o.startDate, o.endDate, u.username
            ORDER BY o.startDate DESC;"""
    
    cursor.execute(query, (username,))
    data = cursor.fetchall()

     # Przetwarzanie wyników (zamiana timedelta na string oraz Decimal na float)
    for order in data:
        for key, value in order.items():
            if isinstance(value, datetime): # Jeśli wartość to timedelta
                order[key] = str(value)      # Zamień na string w formacie "HH:MM:SS"
            if isinstance(value, Decimal):   # Jeśli wartość to Decimal
                order[key] = float(value)    # Zamień na float


    # Dodanie kolumny - numer zamówienia
    for index, row in enumerate(data, start=1):
        row["row_num"] = index
        if row["endDate"] == None: # Zamiana Null na '-'
            row["endDate"] = '-'

    data = json.dumps(data)

    cursor.close()
    database.close()

    return data