// Variable para almacenar los productos en el carrito
let carrito = [];

// Función para añadir productos al carrito
function addToCart(productName, priceBtc) {
    const existingProduct = carrito.find(item => item.name === productName);

    if (existingProduct) {
        existingProduct.quantity += 1;
        existingProduct.total = existingProduct.price_btc * existingProduct.quantity;
    } else {
        carrito.push({
            name: productName,
            price_btc: priceBtc,
            quantity: 1,
            total: priceBtc
        });
    }

    updateCart();
}

// Función para actualizar el carrito
function updateCart() {
    const carritoItems = document.getElementById('carrito-items');
    const totalBtcElement = document.getElementById('total-btc');

    carritoItems.innerHTML = '';

    let totalBtc = 0;

    carrito.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.price_btc.toFixed(8)} BTC</td>
            <td>${item.quantity}</td>
            <td>${item.total.toFixed(8)} BTC</td>
            <td><a href="#" class="borrar" onclick="removeFromCart('${item.name}')">❌</a></td>
        `;
        carritoItems.appendChild(row);
        totalBtc += item.total;
    });

    totalBtcElement.textContent = `${totalBtc.toFixed(8)} BTC`;
}

// Función para eliminar productos del carrito
function removeFromCart(productName) {
    carrito = carrito.filter(item => item.name !== productName);
    updateCart();
}

// Función para generar la factura
function generateInvoice() {
    const customerName = document.getElementById('customer_name').value;
    const email = document.getElementById('email').value;

    if (!customerName || !email) {
        alert('Por favor, completa todos los campos obligatorios.');
        return;
    }

    if (carrito.length === 0) {
        alert('El carrito está vacío. Añade productos antes de generar la factura.');
        return;
    }

    const totalBtc = carrito.reduce((sum, item) => sum + item.total, 0);

    fetch('http://localhost:5000/generate_invoice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            customer_name: customerName,
            email: email,
            items: carrito,
            total_btc: totalBtc
        })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `factura_${customerName.replace(' ', '_')}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al generar la factura. Asegúrate de que el servidor de Python esté en ejecución.');
    });
}

// Inicializar el swiper
document.addEventListener('DOMContentLoaded', function() {
    const swiper = new Swiper('.mySwiper', {
        loop: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    // Asegurarse de que los botones de "Añadir al carrito" funcionen
    document.querySelectorAll('.btn-3').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
        });
    });
});