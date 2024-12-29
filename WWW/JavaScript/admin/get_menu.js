function get_menu() {
    fetch("http://localhost:2500/menu", {method: "GET"})
    .then(response => response.json()) 
    .then(data => {
        display_menu(data)
    });
}


function display_menu(data) {
    const container = document.getElementById("container"); // Kontener na dane menu
    container.innerHTML = ""; // Czyścimy kontener przed dodaniem nowych danych
    
    // Iterujemy przez dane
    data.forEach(menu => {
        // Tworzymy formularz
        const form = document.createElement('form');

        // Nagłówek formularza
        const header = document.createElement('h1');
        header.textContent = menu.name;
        form.appendChild(header);

        // Dane do formularza (etykiety i typy inputów)
        const fields = [
        { label: 'Nazwa', type: 'text', id: `name${menu.menu_id}`, value: menu.name, dataID: 'name'},
        { label: 'Cena', type: 'text', id: `price${menu.menu_id}`, value: menu.price, dataID: 'price' },
        { label: 'Opis', type: 'text', id: `description${menu.menu_id}`, value: menu.description, dataID: 'description' },
        { label: 'Zdjęcie', type: 'text', id: `image${menu.menu_id}`, value: menu.img_url, dataID: 'img_url' }];

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
            button.onclick = () => change_data(field.id, field.dataID, menu.name);
            buttonTextDiv.appendChild(button);
    
            item.appendChild(buttonTextDiv);
            form.appendChild(item);
        })

        
            // Przycisk usunięcia konta
            const deleteButton = document.createElement('button');
            deleteButton.className = 'delete'
            deleteButton.type = 'button'
            deleteButton.textContent = 'Usuń pozycje';
            deleteButton.onclick = () => delete_menu(menu.name);
            form.appendChild(deleteButton);
           

            // Dodanie formularza do container
            container.appendChild(form); 
    })
}

get_menu();


function change_data(elementID, dataID, name) {

    const data = document.getElementById(elementID).value
    const data_to_send = {
        menu_name : name,
        field : dataID,
        value : data
    };

    fetch("http://localhost:2500/menu", {
        method: "PUT", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_send),
    });
}


function search_menu() {
    const menu = document.getElementById('search-input').value

    // Tworzenie URL z parametrami
    const url = `http://localhost:2500/search/menu?menu=${encodeURIComponent(menu)}`;


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
            display_menu(data)
        } else {
            display_menu([data])   
        }
        
    });
}

function delete_menu(name) {
    const data_to_send = {
        'menu' : name
    }
    fetch("http://localhost:2500/menu", {
        method: "DELETE", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_send),
    });
    location.reload()
}

function add_menu() {
    const name = document.getElementById('add-name').value
    const price = document.getElementById('add-price').value
    const desc = document.getElementById('add-description').value
    const url = document.getElementById('add-url').value

    const data_to_send = {
        'name' : name,
        'price' : price,
        'description' : desc,
        'img_url' : url
    }

    fetch("http://localhost:2500/menu", {
        method: "POST", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_send),
    })

}