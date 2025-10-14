function handleCart() {
    const plus = document.getElementById('cart-plus');
    const minus = document.getElementById('cart-minus');
    const quantityInput = document.querySelector('input[type="number"]');
    let quantity = parseInt(quantityInput.value);

    plus.addEventListener('click', () => {
        quantity += 1;
        quantityInput.value = quantity;
    });
    minus.addEventListener('click', () => {
        if (quantity > 1) {
            quantity -= 1;
            quantityInput.value = quantity;
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    handleCart();
});