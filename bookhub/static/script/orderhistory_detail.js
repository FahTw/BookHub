document.addEventListener('DOMContentLoaded', function () {
    let currentRating = 0;

    // Star rating functionality
    const starButtons = document.querySelectorAll('.star-btn');
    starButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            currentRating = parseInt(this.dataset.rating);
            updateStars();
        });

        button.addEventListener('mouseenter', function () {
            const rating = parseInt(this.dataset.rating);
            highlightStars(rating);
        });
    });

    document.getElementById('starRating').addEventListener('mouseleave', function () {
        updateStars();
    });

    function updateStars() {
        starButtons.forEach((button, index) => {
            if (index < currentRating) {
                button.classList.remove('text-gray-300');
                button.classList.add('text-yellow-400');
            } else {
                button.classList.remove('text-yellow-400');
                button.classList.add('text-gray-300');
            }
        });
    }

    function highlightStars(rating) {
        starButtons.forEach((button, index) => {
            if (index < rating) {
                button.classList.remove('text-gray-300');
                button.classList.add('text-yellow-400');
            } else {
                button.classList.remove('text-yellow-400');
                button.classList.add('text-gray-300');
            }
        });
    }

    // Review modal
    window.openReviewModal = function () {
        document.getElementById('reviewModal').classList.remove('hidden');
    };

    window.closeReviewModal = function () {
        document.getElementById('reviewModal').classList.add('hidden');
        // Reset form
        currentRating = 0;
        updateStars();
        document.getElementById('reviewComment').value = '';
    };

    // Review form submission
    document.getElementById('reviewForm').addEventListener('submit', function (e) {
        e.preventDefault();
        if (currentRating === 0) {
            alert('กรุณาให้คะแนน');
            return;
        }

        // Simulate review submission
        setTimeout(() => {
            alert('ขอบคุณสำหรับรีวิว! รีวิวของคุณจะแสดงหลังจากได้รับการตรวจสอบ');
            closeReviewModal();
        }, 500);
    });

    // Add to favorites functionality
    const favoriteButtons = document.querySelectorAll('[data-action="favorite"]');
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const isActive = this.classList.contains('text-red-500');

            if (isActive) {
                this.classList.remove('text-red-500', 'bg-red-50');
                this.classList.add('text-orange-700', 'bg-orange-50');
                this.innerHTML = `
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                            เพิ่มในรายการโปรด
                        `;
            } else {
                this.classList.remove('text-orange-700', 'bg-orange-50');
                this.classList.add('text-red-500', 'bg-red-50');
                this.innerHTML = `
                            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                            ลบจากรายการโปรด
                        `;
            }
        });
    });

    // Buy again functionality
    const buyAgainButtons = document.querySelectorAll('[data-action="buy-again"]');
    buyAgainButtons.forEach(button => {
        button.addEventListener('click', function () {
            if (confirm('คุณต้องการเพิ่มสินค้านี้ลงในตะกร้าหรือไม่?')) {
                // Simulate adding to cart
                setTimeout(() => {
                    alert('เพิ่มสินค้าในตะกร้าเรียบร้อยแล้ว');
                    // Update cart badge
                    const cartBadge = document.querySelector('.bg-orange-600');
                    if (cartBadge) {
                        const currentCount = parseInt(cartBadge.textContent) || 0;
                        cartBadge.textContent = currentCount + 1;
                    }
                }, 500);
            }
        });
    });

    // Download receipt functionality
    const downloadButtons = document.querySelectorAll('[data-action="download"]');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Simulate download progress
            const originalText = button.innerHTML;
            button.innerHTML = `
                        <svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        กำลังดาวน์โหลด...
                    `;
            button.disabled = true;

            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
                alert('ดาวน์โหลดใบเสร็จเรียบร้อยแล้ว!');
            }, 2000);
        });
    });

    // Support contact functionality
    const supportButtons = document.querySelectorAll('[data-action="support"]');
    supportButtons.forEach(button => {
        button.addEventListener('click', function () {
            const options = [
                'โทรศัพท์: 02-123-4567',
                'อีเมล: support@bookhub.com',
                'แชทสด (09:00-18:00)'
            ];

            const choice = confirm(
                'เลือกวิธีการติดต่อฝ่ายสนับสนุน:\n\n' +
                '✓ กด OK เพื่อโทรศัพท์\n' +
                '✗ กด Cancel เพื่อส่งอีเมล'
            );

            if (choice) {
                window.open('tel:02-123-4567', '_self');
            } else {
                window.open('mailto:support@bookhub.com?subject=เกี่ยวกับคำสั่งซื้อ ORD123456&body=สวัสดีครับ/ค่ะ ต้องการสอบถามเกี่ยวกับคำสั่งซื้อ ORD123456', '_blank');
            }
        });
    });

    // Payment receipt view
    const receiptButtons = document.querySelectorAll('[data-action="view-receipt"]');
    receiptButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Simulate opening receipt modal
            alert('กำลังเปิดหลักฐานการชำระเงิน...\n\nรูปแบบ: สลิปโอนเงิน\nวันที่: 15 ตุลาคม 2024\nจำนวนเงิน: ฿940');
        });
    });

    // Copy functionality for reference numbers
    document.addEventListener('click', function (e) {
        if (e.target.textContent === 'คัดลอก') {
            const textToCopy = e.target.previousElementSibling.textContent;
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = e.target.textContent;
                e.target.textContent = 'คัดลอกแล้ว!';
                e.target.classList.add('text-green-600');

                setTimeout(() => {
                    e.target.textContent = originalText;
                    e.target.classList.remove('text-green-600');
                }, 2000);
            }).catch(() => {
                alert('ไม่สามารถคัดลอกได้ กรุณาคัดลอกด้วยตนเอง: ' + textToCopy);
            });
        }
    });

    // Print functionality
    window.addEventListener('beforeprint', function () {
        // Hide navigation and buttons before printing
        const hideElements = document.querySelectorAll('header, .sticky, [data-action]');
        hideElements.forEach(el => {
            el.style.display = 'none';
        });
    });

    window.addEventListener('afterprint', function () {
        // Restore elements after printing
        const showElements = document.querySelectorAll('header, .sticky, [data-action]');
        showElements.forEach(el => {
            el.style.display = '';
        });
    });
});