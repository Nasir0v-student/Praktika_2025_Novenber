

document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
});

function loadProducts() {
    fetch('/api/product/all')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(products => {
            displayProducts(products);
        })
        .catch(error => {
            console.error('Error loading products:', error);
            document.getElementById('products').innerHTML = `
                <div class="col-12 text-center">
                    <div class="alert alert-danger" role="alert">
                        <h4 class="alert-heading">Ошибка загрузки товаров</h4>
                        <p>Пожалуйста, попробуйте обновить страницу или обратитесь в поддержку.</p>
                    </div>
                </div>
            `;
        });
}

function displayProducts(products) {
    const productsContainer = document.getElementById('products');
    
    if (!products || products.length === 0) {
        productsContainer.innerHTML = `
            <div class="col-12 text-center">
                <div class="alert alert-info" role="alert">
                    <h4 class="alert-heading">Товары временно отсутствуют</h4>
                    <p>Загляните к нам позже, мы обязательно пополним ассортимент!</p>
                </div>
            </div>
        `;
        return;
    }

    productsContainer.innerHTML = products.map(product => `
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="card h-100 shadow-sm">
                <img src="${product.photo || 'https://via.placeholder.com/300x400/6c757d/ffffff?text=Нет+изображения'}" 
                     class="card-img-top" alt="${product.name}" 
                     style="height: 300px; object-fit: cover;"
                     onerror="this.src='https://via.placeholder.com/300x400/6c757d/ffffff?text=Нет+изображения'">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text flex-grow-1">${product.description || 'Описание отсутствует'}</p>
                    <div class="mt-auto">
                        <p class="card-text"><strong>Цена: ${product.price} руб.</strong></p>
                        <button class="btn btn-primary w-100" onclick="addToCart(${product.id})">
                            Добавить в корзину
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function addToCart(productId) {
    // Здесь можно добавить логику для корзины
    alert('Товар добавлен в корзину!');
    
    // Пример реализации корзины:
    // let cart = JSON.parse(localStorage.getItem('cart')) || [];
    // const existingItem = cart.find(item => item.id === productId);
    // if (existingItem) {
    //     existingItem.quantity += 1;
    // } else {
    //     cart.push({ id: productId, quantity: 1 });
    // }
    // localStorage.setItem('cart', JSON.stringify(cart));
}

function searchProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const productCards = document.querySelectorAll('.card');
    
    productCards.forEach(card => {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        const description = card.querySelector('.card-text').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            card.parentElement.style.display = 'block';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
}