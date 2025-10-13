document.addEventListener('DOMContentLoaded', function () {
    // Search functionality
    const searchInput = document.querySelector('input[type="text"]');
    const statusSelect = document.querySelector('select');

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const searchTerm = this.value.toLowerCase();
            filterOrders(searchTerm, statusSelect.value);
        });
    }

    if (statusSelect) {
        statusSelect.addEventListener('change', function () {
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            filterOrders(searchTerm, this.value);
        });
    }

    // Cancel order functionality
    const cancelButtons = document.querySelectorAll('button:contains("ยกเลิกคำสั่งซื้อ")');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function () {
            if (confirm('คุณต้องการยกเลิกคำสั่งซื้อนี้หรือไม่?')) {
                // Handle order cancellation
                alert('คำสั่งซื้อถูกยกเลิกแล้ว');
                // Reload or update the page
                location.reload();
            }
        });
    });

    // Reorder functionality
    const reorderButtons = document.querySelectorAll('button:contains("สั่งซื้อใหม่")');
    reorderButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Add items to cart and redirect
            alert('เพิ่มสินค้าในตะกร้าแล้ว');
            window.location.href = '/cart';
        });
    });

    function filterOrders(searchTerm, status) {
        const orderCards = document.querySelectorAll('.bg-white.rounded-lg.shadow-sm');
        let visibleCount = 0;

        orderCards.forEach(card => {
            if (card.id === 'empty-orders') return;

            const orderText = card.textContent.toLowerCase();
            const orderStatus = card.querySelector('.inline-flex').textContent.toLowerCase();

            const matchesSearch = !searchTerm || orderText.includes(searchTerm);
            const matchesStatus = !status || orderStatus.includes(getStatusText(status));

            if (matchesSearch && matchesStatus) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Show empty state if no orders match
        const emptyState = document.getElementById('empty-orders');
        if (visibleCount === 0) {
            emptyState.classList.remove('hidden');
        } else {
            emptyState.classList.add('hidden');
        }
    }

    function getStatusText(status) {
        const statusMap = {
            'pending': 'รอดำเนินการ',
            'processing': 'กำลังประมวลผล',
            'shipped': 'จัดส่งแล้ว',
            'delivered': 'ส่งมอบแล้ว',
            'cancelled': 'ยกเลิกแล้ว'
        };
        return statusMap[status] || '';
    }
});