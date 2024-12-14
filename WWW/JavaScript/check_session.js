function checkSession() {
    fetch("http://localhost:2500/check_session", {method: "GET", credentials: 'include'})  // Wysyłamy zapytanie do Flaskowego endpointu
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status == 'logged_in') {
                document.getElementById('loginButton').innerText = 'Profil';
                document.getElementById('loginButton').href = '/WWW/profile/profile.html';
       
            } else {
                document.getElementById('loginButton').innerText = 'Zaloguj się';
                document.getElementById('loginButton').href = '/WWW/login/login.html';
            }
        });
}

// Uruchamiamy funkcję po załadowaniu strony
window.onload = checkSession;