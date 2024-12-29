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
        elif username == 'admin':
            print("200: Pomyslnie zalogowano")
            session['username'] = username
            return redirect(location=f"{local_url}admin/users/users.html")
        else:
            print("200: Pomyslnie zalogowano")
            session.permanent = True
            session['username'] = username # zapisanie w sesji
            return redirect(location=f"{local_url}home/home.html")
    else:
        print("400: Podaj nazwe uzytkownika oraz haslo")
        return redirect(location=f"{local_url}login/login.html")
    
@app.route("/logout", methods=["GET"])
def logout():
    session.pop('username')
    if 'username' in session:
        return jsonify({'status': 'logged_in'})
    else:
        return jsonify({'status': 'logged_out'})

@app.route("/register", methods=["POST"])
def register():
    # Pobieranie danych od klienta
    data = request.json

    username = data.get('username')
    password = data.get('password')
    password_check = data.get('password2')
    phone = data.get('phone')
    email = data.get('email')

    if database.check_username(username) != None:
        return jsonify({'status': 'failed',
                        'details': 'Konto o podanej nazwie już istnieje'})
    elif password != password_check:
         return jsonify({'status': 'failed',
                        'details': 'Podane hasła nie zgadzaja się'})
    elif database.create_user(username, password, email, phone) == 'success':
        return jsonify({'status': 'success',
                        'details': 'Pomyślnie stworzono konto'})

@app.route('/session', methods=['GET'])
def check_session():
    # Sprawdzamy, czy użytkownik jest zalogowany
    print(session)
    if 'username' in session:
        return jsonify({'status': 'logged_in',
                        'user': session['username']})
    else:
        return jsonify({'status': 'not_logged_in'})
    
@app.route('/menu', methods=['GET'])
def get_menu():
    data = database.get_menu()
    return data

@app.route('/menu', methods=['PUT'])
def change_menu():
    data = request.json

    name = data.get('menu_name')
    key = data.get('field')
    value = data.get('value')
   
    database.change_menu(key, value, name)
    return "200 Dane zostały zmienione"

@app.route('/menu', methods=['DELETE'])
def delete_menu():
    data = request.json
    database.delete_menu_from_db(data['menu'])
    return 'success'

@app.route('/menu', methods=['POST'])
def add_to_menu():
    data = request.json
    database.create_menu(data['name'], data['price'], data['description'], data['img_url'])
    return 'success'

@app.route('/profile', methods=['GET'])
def get_user():
    if 'username' in session:
        user = session['username']
        data = database.get_user_data(user)
        return data
    else:
        return jsonify({'status': 'not_logged_in'})

@app.route('/profile/order_history' , methods=['GET'])
def get_order_history():
    if 'username' in session:
        user = session['username']
        data = database.get_order_history(user)
        return data
    else:
        return jsonify({'status': 'not_logged_in'})

@app.route('/user', methods=['PUT'])
def change_user_data():
    data = request.json

    username = data.get('user')
    key = data.get('field')
    value = data.get('value')
   
    database.change_user_data(key, value, username)
    return "200 Dane zostały zmienione"

@app.route('/user', methods=['DELETE'])
def delete_user():
    data = request.json
    database.delete_user_from_db(data['user'])
    return 'success'

@app.route('/order', methods=['POST'])
def make_order():
    data = request.get_json()

    city = data.get('city')
    street = data.get('street')
    apartment_num = data.get('apartment_num')
    phone = data.get('phone')

    if 'username' in session:
        status = database.make_order(session['username'], data['items'], city, street, apartment_num, phone)
    else:
        status = database.make_order(None, data['items'], city, street, apartment_num, phone)
    return jsonify({'status' : status})

@app.route('/order', methods=['PUT'])
def change_order_status():
    data = request.json
    database.change_status(data['status'],data['id'])
    return 'success'

@app.route('/users', methods=['GET'])
def get_users():
    data = database.get_users_data()
    return data

@app.route('/search/user', methods=['GET'])
def search_user():
    data = request.args.get('user')
    if data == '':
        users = database.get_users_data()
        return users
    else:
        user = database.get_user_data(data)
        return user

@app.route('/search/menu', methods=['GET'])
def search_menu():
    data = request.args.get('menu')
    print(data)
    if data == '':
        menu = database.get_menu()
        return menu
    else:
        pos = database.get_position_from_menu(data)
        return pos

@app.route('/orders', methods=['GET'])
def get_orders():
    data = database.get_orders()
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2500)
