// Quantity controls
document.addEventListener('DOMContentLoaded', function () {
    // Quantity increase/decrease functionality
    const quantityControls = document.querySelectorAll('[data-action]');

    quantityControls.forEach(button => {
        button.addEventListener('click', function () {
            const action = this.dataset.action;
            const quantitySpan = action === 'increase' ?
                this.previousElementSibling :
                this.nextElementSibling;

            let currentQuantity = parseInt(quantitySpan.textContent);

            if (action === 'increase') {
                currentQuantity++;
            } else if (action === 'decrease' && currentQuantity > 1) {
                currentQuantity--;
            }

            quantitySpan.textContent = currentQuantity;
            updateTotal();
        });
    });

    // Remove item functionality
    const removeButtons = document.querySelectorAll('[data-remove]');
    removeButtons.forEach(button => {
        button.addEventListener('click', function () {
            if (confirm('คุณต้องการลบสินค้านี้ออกจากตะกร้าหรือไม่?')) {
                this.closest('.cart-item').remove();
                updateTotal();
                checkEmptyCart();
            }
        });
    });

    // Select all checkbox functionality
    const selectAllCheckbox = document.querySelector('#select-all');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function () {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateTotal();
        });
    }

    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateTotal);
    });

    function updateTotal() {
        let total = 0;
        let itemCount = 0;

        itemCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const price = parseFloat(checkbox.closest('.cart-item').dataset.price || 350);
                const quantity = parseInt(checkbox.closest('.cart-item').querySelector('[data-quantity]')?.textContent || 1);
                total += price * quantity;
                itemCount += quantity;
            }
        });

        // Update summary
        const subtotalElement = document.querySelector('[data-subtotal]');
        const totalElement = document.querySelector('[data-total]');
        const itemCountElement = document.querySelector('[data-item-count]');
        const dataItemTotal = document.querySelector('[data-item-total]');

        if (subtotalElement) subtotalElement.textContent = `฿${total}`;
        if (totalElement) totalElement.textContent = `฿${total}`;
        if (itemCountElement) itemCountElement.textContent = `${itemCount} รายการ`;
        if (dataItemTotal) dataItemTotal.textContent = `${total}`;
    }

    function checkEmptyCart() {
        const cartItems = document.querySelectorAll('.cart-item');
        const emptyCartState = document.getElementById('empty-cart');
        const cartContent = document.querySelector('main');

        if (cartItems.length === 0) {
            cartContent.classList.add('hidden');
            emptyCartState.classList.remove('hidden');
        }
    }
});