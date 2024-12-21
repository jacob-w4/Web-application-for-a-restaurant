function checkSession() {
    fetch("http://localhost:2500/check_session", {method: "GET", credentials: 'include'})  // Wysyłamy zapytanie do Flaskowego endpointu
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status == 'logged_in') {
                document.getElementById('profileButton').innerText = `Profil (${data.user})`

                document.getElementById('logoutButton').style.display = 'flex';
                document.getElementById('profileButton').style.display = 'flex';
                document.getElementById('loginButton').style.display = 'none';
       
            } else {
                document.getElementById('logoutButton').style.display = 'none';
                document.getElementById('profileButton').style.display = 'none';
                document.getElementById('loginButton').style.display = 'flex';
            }
        });
}

// Uruchamiamy funkcję po załadowaniu strony
window.onload = checkSession;

function logout() {
    fetch("http://localhost:2500/logout", {method: "GET", credentials: 'include'})
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status == 'logged_out') {
            window.location = "http://127.0.0.1:2501/WWW/home/home.html"
        }   
    });
}