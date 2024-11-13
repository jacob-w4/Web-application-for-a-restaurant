from flask import Flask, request, redirect

app = Flask(__name__)

remote_url = "http://20.215.201.137/"
local_url = "http://localhost:63342/C:/Users/Jakub/VscProject/lokal_kebab/WWW/"


@app.route("/login", methods=["POST"])
def login():
    # Pobieranie danych od klienta
    username = request.form['username']
    password = request.form['password']

    # Logowanie i przekierowanie do home
    if username != "" and password != "":
        user = (username, password)

        print("Data has been sent")
        return redirect(location=f"{local_url}home/home.html")
        # return redirect(location=f"{remote_url}home.html")
    else:
        print("Error: Enter username and password")
        return redirect(location=f"{local_url}login/login.html")
        # return redirect(location=remote_url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2500)
