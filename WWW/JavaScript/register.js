function register() {
    const username = document.getElementsByName('username')[0].value; // [0] bo getElementsByName zwraca listę
    const password = document.getElementsByName('password')[0].value;
    const password2 = document.getElementsByName('password2')[0].value;
    const email = document.getElementsByName('email')[0].value;
    const phone = document.getElementsByName('phone')[0].value;

    const data = {
        'username': username,
        'password': password,
        'password2': password2,
        'email': email,
        'phone': phone
    };

    fetch("http://jakubplewa.pl/api/register", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json()) // Dekodowanie JSON z odpowiedzi
    .then(result => {
        
        if (result.status === 'failed' && result.details === 'Konto o podanej nazwie już istnieje') {
 
            console.log(result)
            document.getElementById('status').innerText = `Błąd: ${result.details}`;
           
        } 
        if (result.status === 'failed' && result.details === 'Podane hasła nie zgadzaja się') {

            console.log(result)
            document.getElementById('status').innerText = `Błąd: ${result.details}`;

        } 
        if (result.status === 'success') {
            console.log(result)
            window.location = "http://jakubplewa.pl/login/login.html";
        }
    })
    .catch(error => {
        console.error("Błąd podczas rejestracji:", error);
    });
}
