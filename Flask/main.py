from flask import Flask, jsonify, request, redirect, session
import db as database
from datetime import timedelta

app = Flask(__name__)

# klucz oraz czas trwania sesji
app.config['SECRET_KEY'] = 'hadhdhgfvcjrtfj'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

local_url = "http://jakubplewa.pl:80/"


@app.route("/api/login", methods=["POST"])
def login():
    # Pobieranie danych od klienta
    username = request.form['username']
    password = request.form['password']

    # Logowanie i przekierowanie do home (strona glowna)
    if username != "" and password != "":

        # Zapytanie do bazy danych
        user = database.get_user(username, password)
       
        if user is None: # Gdy podany użytkownik nie istnieje
            return redirect(location=f"{local_url}login/login.html")
        elif username == 'admin': # Dla administratora
            session['username'] = username
            return redirect(location=f"{local_url}admin/users/users.html")
        else: # W innym wypadku pomyślne logowanie
            session.permanent = True
            session['username'] = username
            return redirect(location=f"{local_url}home/home.html")
    else: # Gdy pola nie zostały wypełnione
        return redirect(location=f"{local_url}login/login.html")
    
@app.route("/api/logout", methods=["GET"])
def logout():
    session.pop('username')
    if 'username' in session: # Gdy Uzytkownik jest zalogowany
        return jsonify({'status': 'logged_in'})
    else:
        return jsonify({'status': 'logged_out'})

@app.route("/api/register", methods=["POST"])
def register():
    # Pobieranie danych od klienta
    data = request.json

    username = data.get('username')
    password = data.get('password')
    password_check = data.get('password2')
    phone = data.get('phone')
    email = data.get('email')

    if username != "" and password != "" and password_check != "" and phone != "" and email != "": # Sprawdza czy wszystkie pola zostały wypełnione
        if database.check_username(username) != None: # Użytkownik już istnieje
            return jsonify({'status': 'failed',
                        'details': 'Konto o podanej nazwie już istnieje'})
        elif password != password_check:
            return jsonify({'status': 'failed',
                        'details': 'Podane hasła nie zgadzaja się'})
        elif database.create_user(username, password, email, phone) == 'success':
            return jsonify({'status': 'success',
                        'details': 'Pomyślnie stworzono konto'})
    else: # Gdy pola nie zostały wypełnione
        return jsonify({'status': 'failed',
                        'details': 'Wypełnij wszystkie pola'})

@app.route('/api/session', methods=['GET'])
def check_session():
    # Sprawdzamy, czy użytkownik jest zalogowany
    if 'username' in session:
        return jsonify({'status': 'logged_in',
                        'user': session['username']})
    else:
        return jsonify({'status': 'not_logged_in'})
    
@app.route('/api/menu', methods=['GET'])
def get_menu():
    # Pobiera dane z bazy i zwraca do front
    data = database.get_menu()
    return data

@app.route('/api/menu', methods=['PUT'])
def change_menu():
    # Pobieranie danych od klienta
    data = request.json

    name = data.get('menu_name')
    key = data.get('field')
    value = data.get('value')
   
   # Zamiana pozycji w menu
    database.change_menu(key, value, name)
    return "200 Dane zostały zmienione"

@app.route('/api/menu', methods=['DELETE'])
def delete_menu():
    # Pobieranie danych od klienta
    data = request.json
    message = database.delete_menu_from_db(data['menu']) # Zwraca None podczas błędu
    if message != "": 
        return jsonify({'status' : 'success'})
    else:
        return jsonify({'status' : 'failed'})

@app.route('/api/menu', methods=['POST'])
def add_to_menu():
    # Pobieranie danych od klienta
    data = request.json
    if data != "": # Wypełnione pola
        message = database.create_menu(data['name'], data['price'], data['description'], data['img_url']) # Zwraca None podczas błędu
        if message != "":
            return jsonify({'status' : 'success'})
        else:
            return jsonify({'status' : 'failed'})   
    else: 
        return jsonify({'status' : 'failed',
                        'details' : 'Wypełnij wszystkie pola'})  

@app.route('/api/profile', methods=['GET'])
def get_user():
    if 'username' in session: # Sprawdza czy użytkownik jest zalogowany
        user = session['username']
        data = database.get_user_data(user)
        return data
    else:
        return jsonify({'status': 'not_logged_in'})

@app.route('/api/profile/order_history' , methods=['GET'])
def get_order_history():
    if 'username' in session: # Sprawdza czy użytkownik jest zalogowany
        user = session['username']
        data = database.get_order_history(user)
        return data
    else:
        return jsonify({'status': 'not_logged_in'})

@app.route('/api/user', methods=['PUT'])
def change_user_data():
    # Pobieranie danych od klienta
    data = request.json

    username = data.get('user')
    key = data.get('field')
    value = data.get('value')
   
    database.change_user_data(key, value, username)
    return "200 Dane zostały zmienione"

@app.route('/api/user', methods=['DELETE'])
def delete_user():
    # Pobieranie danych od klienta
    data = request.json
    message = database.delete_user_from_db(data['user']) # Zwraca None podczas błędu
    if message != "":
        return jsonify({'status' : 'success'})
    else:
        return jsonify({'status' : 'failed'}) 

@app.route('/api/order', methods=['POST'])
def make_order():
    # Pobieranie danych od klienta
    data = request.get_json()

    city = data.get('city')
    street = data.get('street')
    apartment_num = data.get('apartment_num')
    phone = data.get('phone')

    if city != "" and street != "" and apartment_num != "" and phone != "":
        if 'username' in session:
            status = database.make_order(session['username'], data['items'], city, street, apartment_num, phone) # Zwraca odpowiedni status
        else: # Dla niezalogowanych uzytkowników
            status = database.make_order(None, data['items'], city, street, apartment_num, phone) # Zwraca odpowiedni status
        return jsonify({'status' : status})
    else:
        return jsonify({'status' : 'Wypełnij wszystkie pola'})

@app.route('/api/order', methods=['PUT'])
def change_order_status():
    # Pobieranie danych od klienta
    data = request.json
    message = database.change_status(data['status'],data['id']) # Zwraca None podczas błędu
    if message != "":
        return jsonify({'status' : 'success'})
    else:
        return jsonify({'status' : 'failed'})

@app.route('/api/users', methods=['GET'])
def get_users():
    # Pobieranie danych z bazy
    data = database.get_users_data()
    return data

@app.route('/api/search/user', methods=['GET'])
def search_user():
    # Pobieranie danych od klienta
    data = request.args.get('user')
    if data == '': # Zwraca wszyskich użytkowników
        users = database.get_users_data()
        return users
    else: # Zwraca szukanego użytkownika
        user = database.get_user_data(data)
        return user

@app.route('/api/search/menu', methods=['GET'])
def search_menu():
    # Pobieranie danych od klienta
    data = request.args.get('menu')
    if data == '': # Zwraca wszyskie pozycje
        menu = database.get_menu()
        return menu
    else: # Zwraca szukane danie
        pos = database.get_position_from_menu(data)
        return pos

@app.route('/api/orders', methods=['GET'])
def get_orders():
    # Pobieranie danych z bazy
    data = database.get_orders()
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2500)
