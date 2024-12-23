function display_cart() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];

    const orderContainer = document.getElementById("order-list"); // Kontener na dane menu
    orderContainer.innerHTML = ""; // Wyczyść obecny koszyk

    cart.forEach(cartItem =>{
        const orderItem = document.createElement("div");
        orderItem.className = "order-item";

        const itemName = document.createElement("p");
        itemName.className = "order-name";
        itemName.textContent = cartItem.name;

        const rightSection = document.createElement("div");
        rightSection.className = "buttons";

        const priceContainer = document.createElement("p");
        priceContainer.className = "order-price";
        priceContainer.textContent =  `${cartItem.price} zł`;

        const subButton = document.createElement("button");
        subButton.textContent = '-';
        subButton.onclick = function () { 
            cart_substract(cartItem.name)
        }

        subButton.className = "add-button";

        rightSection.appendChild(priceContainer)
        rightSection.appendChild(subButton)

        orderItem.appendChild(itemName)
        orderItem.appendChild(rightSection)

        orderContainer.appendChild(orderItem)
    })
}

function cart_add(item, price) {
    // Pobierz obecny koszyk z localStorage lub ustaw pustą tablicę
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length >= 7) {
        return;
    }
    
    cart.push({'name' : item, 'price' : price})

    localStorage.setItem("cart", JSON.stringify(cart));

    display_cart()
}

function cart_substract(item) {
    // Pobierz obecny koszyk z localStorage lub ustaw pustą tablicę
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    const itemIndex = cart.findIndex(cartItem => cartItem.name === item);
    // usuwanie elementu
    cart.splice(itemIndex, 1);

    localStorage.setItem("cart", JSON.stringify(cart));

    display_cart()
}

display_cart();