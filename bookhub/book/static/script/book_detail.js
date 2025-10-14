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

function handleStarRating() {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    const ratingText = document.getElementById('rating-text');
    let selectedRating = 0;

    stars.forEach((star, index) => {
        // Click to select rating
        star.addEventListener('click', () => {
            selectedRating = parseInt(star.getAttribute('data-rating'));
            ratingInput.value = selectedRating;
            updateStars(selectedRating);
            updateRatingText(selectedRating);
        });

        // Hover effect
        star.addEventListener('mouseenter', () => {
            const hoverRating = parseInt(star.getAttribute('data-rating'));
            updateStars(hoverRating);
        });
    });

    // Reset to selected rating on mouse leave
    const starContainer = document.getElementById('star-rating');
    starContainer.addEventListener('mouseleave', () => {
        updateStars(selectedRating);
    });

    function updateStars(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.remove('text-gray-300');
                star.classList.add('text-orange-400');
            } else {
                star.classList.remove('text-orange-400');
                star.classList.add('text-gray-300');
            }
        });
    }

    function updateRatingText(rating) {
        const ratingLabels = ['', 'แย่มาก', 'ไม่ดี', 'ปานกลาง', 'ดี', 'ดีมาก'];
        ratingText.textContent = rating > 0 ? `${rating} ดาว - ${ratingLabels[rating]}` : 'เลือกคะแนน';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    handleCart();
    handleStarRating();
});