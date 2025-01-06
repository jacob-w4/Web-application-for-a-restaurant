function get_history() {
    fetch("http://jakubplewa.pl/api/profile/order_history", {method: "GET" , credentials: 'include'})
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
            <td>${order.row_num}</td>
            <td>${order.status}</td>
            <td>${order.startDate}</td>
            <td>${order.endDate}</td>
            <td>${order.items}</td>
            <td>${order.total_price}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

get_history();
