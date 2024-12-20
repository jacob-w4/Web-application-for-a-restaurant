function get_user_data() {
    fetch("http://localhost:2500/get_user_profile", {method: "GET", credentials: 'include'})
    .then(response => response.json()) 
    .then(data => {
        document.getElementById("h1").innerText = `Witaj ${data.username}!` 
        document.getElementById("password").value = data.password
        document.getElementById("email").value = data.email
        document.getElementById("city").value = data.city
        document.getElementById("street").value = data.street
        document.getElementById("apartment_num").value = data.apartment_num
        document.getElementById("phone").value = data.phone
    });
}

function change_data(dataID) {

    const data = document.getElementById(dataID).value
    const data_to_send = {
        field : dataID,
        value : data
    };

    fetch("http://localhost:2500/change_user_data", {
        method: "PUT", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_send),
    });
}

// Upewnij się, że funkcja jest widoczna globalnie
window.change_data = change_data


get_user_data();