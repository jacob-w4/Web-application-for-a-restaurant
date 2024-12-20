function get_menu() {
    fetch("http://localhost:2500/get_menu", {method: "GET"})
    .then(response => response.json()) 
    .then(data => {
        const menuContainer = document.getElementById("menu-container"); // Kontener na dane menu
        menuContainer.innerHTML = ""; // Czyścimy kontener przed dodaniem nowych danych
        
        // Iterujemy przez dane
        data.forEach(item => {
            // Tworzymy nowy element HTML dla każdego elementu menu
            const itemContainer = document.createElement("div");
            itemContainer.className = "item"; // Dodanie klasy dla stylizacji

            console.log(item)

            const img = document.createElement("img");
            img.className = "item-img"
            img.src = item.img_url;

            const itemDesc = document.createElement("div");
            itemDesc.className = "item-desc";

            const title = document.createElement("h1");
            title.textContent = item.name;

            const description = document.createElement("p");
            description.textContent = item.description;
            description.className = "desc";

            const price = document.createElement("p");
            price.textContent = `Cena: ${item.price} zł`;
            price.className = "price"

            const button = document.createElement("button")
            button.textContent = 'Zamów'
            button.className = "order-button"
            button.onclick = () => order(item.name, item.price);

            // Tworzenie item-desc
            itemDesc.appendChild(title)
            itemDesc.appendChild(description)
            itemDesc.appendChild(price)
            itemDesc.appendChild(button)

            // Tworzenie item
            itemContainer.appendChild(img)
            itemContainer.appendChild(itemDesc)

            // Dodajemy menu-item do kontenera
            menuContainer.appendChild(itemContainer);
        })
    });
}

function order(item, price) {
    const orderContainer = document.getElementById("order-list"); // Kontener na dane menu

    if (orderContainer.children.length >= 8) {
        return;  // Zatrzymujemy dalsze tworzenie nowych elementów
    }

    const orderItem = document.createElement("div");
    orderItem.className = "order-item";

    const itemName = document.createElement("p");
    itemName.className = "order-name";
    itemName.textContent = item;

    const rightSection = document.createElement("div");
    rightSection.className = "buttons";

    const priceContainer = document.createElement("p");
    priceContainer.className = "order-price";
    priceContainer.textContent =  `${price} zł`;

    const addButton = document.createElement("button");
    addButton.textContent = '+';
    const subButton = document.createElement("button");
    subButton.textContent = '-';
    subButton.onclick = function () { 
        orderItem.remove()
    }

    addButton.className = "add-button";
    subButton.className = "add-button";


    rightSection.appendChild(priceContainer)
    rightSection.appendChild(addButton)
    rightSection.appendChild(subButton)


    orderItem.appendChild(itemName)
    orderItem.appendChild(rightSection)

    orderContainer.appendChild(orderItem)
}


// Uruchamiamy funkcję po załadowaniu strony
get_menu();