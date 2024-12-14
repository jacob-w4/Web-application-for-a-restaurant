import mysql.connector

database = mysql.connector.connect(
    host="jakubplewa.pl",
    user="jakub",
    password="jakub",
    port=3606
)

def get_database_connection():
    if not database.is_connected():
        database.reconnect()  # Odnawianie połączenia
    return database


def get_user(username, password):
    database = get_database_connection()
    cursor = database.cursor()

    # Zapytanie do bazy danych
    query = "SELECT password FROM `lokal-kebab`.Users WHERE username = %s AND password = %s" 
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    return result


