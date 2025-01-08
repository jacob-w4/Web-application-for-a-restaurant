function get_orders() {
    fetch("http://localhost:2500/orders", {method: "GET"})
    .then(response => response.json()) 
    .then(data => {
        display_orders(data)
    });
}

function display_orders(data) {
    const tableBody = document.getElementById('table')
    tableBody.innerHTML = "";


    data.forEach(order => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${order.username}</td>
            <td>${order.status}</td>
            <td>${order.startDate}</td>
            <td>${order.address}</td>
            <td>${order.phone}</td>
            <td>${order.items}</td>
            <td>${order.total_price}</td>
            <td>
                <button class="cancel-order" data-id="cancel${order.order_id}" onclick="cancel(${order.order_id})">Anuluj</button>
                <button class="finish-order" data-id="finish${order.order_id}" onclick="finish(${order.order_id})">x</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
}

get_orders();

function cancel(order_id) {
    data = {
        'status' : 'Anulowano',
        'id' : order_id
    }

    fetch("http://localhost:2500/order", {
        method: "PUT", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.status = 'success') {
            window.location.reload();
        }
    });
}

function finish(order_id) {
    data = {
        'status' : 'Zakończono',
        'id' : order_id
    }

    fetch("http://localhost:2500/order", {
        method: "PUT", 
        credentials: 'include', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.status = 'success') {
            window.location.reload();
        }
    });
}