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

# Ustawienie plików cookies
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True  # Wymagane dla SameSite=None
app.config['SESSION_COOKIE_HTTPONLY'] = True

local_url = "http://127.0.0.1:2501/WWW/"


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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2500)
