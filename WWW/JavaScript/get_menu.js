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
            button.onclick = () => cart_add(item.name, item.price);

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




// Uruchamiamy funkcję po załadowaniu strony
get_menu();
