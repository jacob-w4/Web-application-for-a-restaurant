from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

remote_url = "http://20.215.201.137/"
local_url = "http://127.0.0.1:5200/WWW/"


@app.route("/login", methods=["POST"])
def login():
    # Pobieranie danych od klienta
    username = request.form['username']
    password = request.form['password']

    # Logowanie i przekierowanie do home (strona glowna)
    if username != "" and password != "":
        user = (username, password)

        print("Data has been sent")
        return redirect(location=f"{local_url}home/home.html")
        # return redirect(location=f"{remote_url}home.html")
    else:
        print("Error: Enter username and password")
        return redirect(location=f"{local_url}login/login.html")
        # return redirect(location=remote_url)

@app.route("/profile", methods=["GET"])
def send_data_to_profile():
    return jsonify({
     "username" : "jakub",
     "email" : "xyz@gmail.com",
     "phone" : "XXX-XXX-XXX",
     "points" : "54",
     "city" : "Wrocław",
     "street" : "ul. Kwiatowa 999",
     "apartment_num" : "16"
    })

@app.route("/edit_profile", methods=["PUT"])
def edit_user_data():
    return "Dane pomyślnie zaktualizowane"

@app.route("/order", methods=["POST"])
def make_order():
    return jsonify({"status" : "Zamówienie zostało złożone"})

@app.route("/admin_orders", methods=["GET","PUT","DELETE"])
def orders():
    return jsonify({"status" : "Success"})

@app.route("/admin_change_menu", methods=["POST", "DELETE", "PUT"])
def change_menu():
    return jsonify({"status" : "Success"})

@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify({
     "name" : "kebab w bułce",
     "price" : "19.99",
     "size" : "M",
     "description" : "Kebab w bułce – aromatyczne mięso z rożna, idealnie doprawione i soczyste, podawane w świeżej, chrupiącej bułce. Dopełnieniem smaku są świeże warzywa oraz sosy do wyboru – czosnkowy, ostry lub jogurtowy. Idealna propozycja na szybki, sycący posiłek!"
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2500)
