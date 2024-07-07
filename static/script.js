document.addEventListener('DOMContentLoaded', () => {
    const cart = [];
    const cartModal = new bootstrap.Modal(document.getElementById('cartModal'));

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function () {
            const productElement = this.closest('.product');
            const productName = productElement.getAttribute('data-name');
            const productPrice = parseFloat(productElement.getAttribute('data-price'));
            const productQuantity = parseInt(productElement.querySelector('.quantity').innerText);

            const productInCart = cart.find(item => item.name === productName);

            if (productInCart) {
                productInCart.quantity += productQuantity;
            } else {
                cart.push({ name: productName, price: productPrice, quantity: productQuantity });
            }

            updateCartModal();
            updateCartIcon();
        });
    });

    document.querySelectorAll('.increase').forEach(button => {
        button.addEventListener('click', function () {
            const quantityElement = this.closest('.quantity-controls').querySelector('.quantity');
            let quantity = parseInt(quantityElement.innerText);
            quantityElement.innerText = ++quantity;
        });
    });

    document.querySelectorAll('.decrease').forEach(button => {
        button.addEventListener('click', function () {
            const quantityElement = this.closest('.quantity-controls').querySelector('.quantity');
            let quantity = parseInt(quantityElement.innerText);
            if (quantity > 1) {
                quantityElement.innerText = --quantity;
            }
        });
    });

    document.getElementById('cartIcon').addEventListener('click', function () {
        updateCartModal();
        cartModal.show();
    });

    document.getElementById('checkout').addEventListener('click', async function () {
        if (cart.length === 0) {
            alert('El carrito está vacío.');
            return;
        }

        try {
            const response = await fetch('/orders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ products: cart })
            });

            if (!response.ok) {
                throw new Error('Error al realizar el pedido.');
            }

            const result = await response.json();
            alert('Pedido realizado con éxito. ID del pedido: ' + result.order_id);
            cart.length = 0;
            updateCartModal();
            updateCartIcon();
            cartModal.hide();
        } catch (error) {
            alert(error.message);
        }
    });

    function updateCartModal() {
        const cartItemsList = document.getElementById('cartItems');
        cartItemsList.innerHTML = '';

        cart.forEach((item, index) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                ${item.name} - $${item.price.toFixed(2)}
                <div class="quantity-controls">
                    <button class="btn btn-sm btn-secondary decrease" data-index="${index}">-</button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="btn btn-sm btn-secondary increase" data-index="${index}">+</button>
                </div>
                <button class="btn btn-sm btn-danger remove" data-index="${index}">Eliminar</button>
            `;
            cartItemsList.appendChild(li);
        });

        document.querySelectorAll('.increase').forEach(button => {
            button.addEventListener('click', function () {
                const index = parseInt(this.getAttribute('data-index'));
                cart[index].quantity++;
                updateCartModal();
                updateCartIcon();
            });
        });

        document.querySelectorAll('.decrease').forEach(button => {
            button.addEventListener('click', function () {
                const index = parseInt(this.getAttribute('data-index'));
                if (cart[index].quantity > 1) {
                    cart[index].quantity--;
                }
                updateCartModal();
                updateCartIcon();
            });
        });

        document.querySelectorAll('.remove').forEach(button => {
            button.addEventListener('click', function () {
                const index = parseInt(this.getAttribute('data-index'));
                cart.splice(index, 1);
                updateCartModal();
                updateCartIcon();
            });
        });
    }

    function updateCartIcon() {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        document.getElementById('cartIcon').innerHTML = `<i class="fas fa-shopping-cart"></i> Ver Carrito (${totalItems})`;
    }

    const searchBar = document.getElementById('searchBar');
    const products = document.querySelectorAll('.product');
    const closeModal = document.querySelector('.btn-close');
    const cartItemsList = document.getElementById('cartItems');

    searchBar.addEventListener('input', () => {
        const searchTerm = searchBar.value.toLowerCase();
        products.forEach(product => {
            const productName = product.getAttribute('data-name').toLowerCase();
            product.style.display = productName.includes(searchTerm) ? 'block' : 'none';
        });
    });

    updateCartIcon();
});