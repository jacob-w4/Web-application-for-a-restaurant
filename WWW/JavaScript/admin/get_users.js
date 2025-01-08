function get_users() {
    fetch("http://jakubplewa.pl/api/users", {method: "GET"})
    .then(response => response.json()) 
    .then(data => {
        display_users(data)
    });
}

function display_users(data) {
    const container = document.getElementById("container"); // Kontener na dane menu
    container.innerHTML = ""; // Czyścimy kontener przed dodaniem nowych danych
    
    // Iterujemy przez dane
    data.forEach(user => {
        // Tworzymy formularz
        const form = document.createElement('form');

        // Nagłówek formularza
        const header = document.createElement('h1');
        header.textContent = user.username;
        form.appendChild(header);

        // Dane do formularza (etykiety i typy inputów)
        const fields = [
        { label: 'Hasło', type: 'text', id: `password${user.user_id}`, value: user.password, dataID: 'password'},
        { label: 'Email', type: 'email', id: `email${user.user_id}`, value: user.email, dataID: 'email' },
        { label: 'Miasto', type: 'text', id: `city${user.user_id}`, value: user.city, dataID: 'city' },
        { label: 'Ulica', type: 'text', id: `street${user.user_id}`, value: user.street, dataID: 'street' },
        { label: 'Numer domu', type: 'text', id: `apartment_num${user.user_id}`, value: user.apartment_num, dataID: 'apartment_num' },
        { label: 'Telefon', type: 'tel', id: `phone${user.user_id}`, value: user.phone, dataID: 'phone' }];

        fields.forEach(field => {
            const item = document.createElement('div');
            item.className = 'item'
    
            const label = document.createElement('p');
            label.textContent = field.label;
            item.appendChild(label);
    
            const buttonTextDiv = document.createElement('div');
            buttonTextDiv.className = 'button-text';
    
            const input = document.createElement('input');
            input.type = field.type;
            input.className = 'text';
            input.id = field.id;
            input.value = field.value;
            buttonTextDiv.appendChild(input);
    
            const button = document.createElement('button');
            button.type = 'button';
            button.textContent = '✓';
            button.onclick = () => change_data(field.id, field.dataID, user.username);
            buttonTextDiv.appendChild(button);
    
            item.appendChild(buttonTextDiv);
            form.appendChild(item);
        })

            if (user.username != 'admin') {
                // Przycisk usunięcia konta
                const deleteButton = document.createElement('button');
                deleteButton.className = 'delete'
                deleteButton.textContent = 'Usuń konto';
                deleteButton.type = 'button'
                deleteButton.onclick = () => delete_account(user.username);
                form.appendChild(deleteButton);
            }
           

            // Dodanie formularza do container
            container.appendChild(form); 
    })
}

// Uruchamiamy funkcję po załadowaniu strony
get_users();

function change_data(elementID, dataID, username) {

    const data = document.getElementById(elementID).value
    const data_to_send = {
        user : username,
        field : dataID,
        value : data
    };

    fetch("http://jakubplewa.pl/api/user", {
        method: "PUT", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_send),
    });
}

function delete_account(username) {
    const data_to_send = {
        user : username
    }
    fetch("http://jakubplewa.pl/api/user", {
        method: "DELETE", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_send),
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.status = 'success') {
            window.location.reload();
        }
    });
}

function search_user() {
    const user = document.getElementById('search-input').value

    // Tworzenie URL z parametrami
    const url = `http://jakubplewa.pl/api/search/user?user=${encodeURIComponent(user)}`;


    fetch(url, {
        method: "GET", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then (response => response.json())
    .then (data => {
        if(data.length > 1) {
            display_users(data)
        } else {
            display_users([data])   
        }
        
    });
}