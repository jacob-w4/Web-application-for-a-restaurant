from flask import Flask, jsonify, request, redirect, session
import db as database
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)

# klucz oraz czas trwania sesji
app.config['SECRET_KEY'] = 'hadhdhgfvcjrtfj'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

# Obsługa róznych domen/portów
CORS(app, origins=["http://127.0.0.1:2501"], supports_credentials=True)
#CORS(app, supports_credentials=True, origins=["http://jakubplewa.pl"])

# Ustawienie plików cookies - lokalnie
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True # Wymagane dla SameSite=None
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Ustawienie plików cookies - serwer Linux
#app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
#app.config['SESSION_COOKIE_SECURE'] = False
#app.config['SESSION_COOKIE_HTTPONLY'] = True


local_url = "http://127.0.0.1:2501/WWW/"
#local_url = "http://jakubplewa.pl:80/"


@app.route("/login", methods=["POST"])
def login():
    # Pobieranie danych od klienta
    username = request.form['username']
    password = request.form['password']

    # Logowanie i przekierowanie do home (strona glowna)
    if username != "" and password != "":

        # Zapytanie do bazy danych
        user = database.get_user(username, password)
       
        if user is None:
            print("404: Uzytkownik nie istnieje")
            return redirect(location=f"{local_url}login/login.html")
        else:
            print("200: Pomyslnie zalogowano")
            session.permanent = True
            session['username'] = username # zapisanie w sesji
            return redirect(location=f"{local_url}home/home.html")
    else:
        print("400: Podaj nazwe uzytkownika oraz haslo")
        return redirect(location=f"{local_url}login/login.html")


@app.route('/check_session', methods=['GET'])
def check_session():
    # Sprawdzamy, czy użytkownik jest zalogowany
    print(session)
    if 'username' in session:
        return jsonify({'status': 'logged_in'})
    else:
        return jsonify({'status': 'not_logged_in'})
    

@app.route('/get_menu', methods=['GET'])
def get_menu():
    data = database.get_menu()
    return data


@app.route('/get_user_profile', methods=['GET'])
def get_user():
    user = session['username']
    data = database.get_user_data(user)
    return data


@app.route('/change_user_data', methods=['PUT'])
def change_user_data():
    data = request.json

    key = data.get('field')
    value = data.get('value')
   
    database.change_user_data(key, value, session['username'])
    return "200 Dane zostały zmienione"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2500)
