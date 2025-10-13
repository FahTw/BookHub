document.addEventListener('DOMContentLoaded', function () {
    // Get search input and status select elements
    const searchInput = document.querySelector('input[type="text"]');
    const statusSelect = document.querySelector('select');

    // Add event listener for search input
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const searchTerm = this.value.toLowerCase();
            const selectedStatus = statusSelect ? statusSelect.value : '';
            filterOrders(searchTerm, selectedStatus);
        });
    }

    // Add event listener for status select
    if (statusSelect) {
        statusSelect.addEventListener('change', function () {
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            const selectedStatus = this.value;
            filterOrders(searchTerm, selectedStatus);
        });
    }

    function filterOrders(searchTerm, statusFilter) {
        const orderCards = document.querySelectorAll('.bg-white.rounded-lg.shadow-sm.overflow-hidden.border');
        let visibleCount = 0;

        orderCards.forEach(card => {
            // Get book title from h4 element (not order number)
            const bookTitleElement = card.querySelector('h4.font-semibold.text-gray-900');
            const bookTitle = bookTitleElement ? bookTitleElement.textContent.toLowerCase() : '';
            
            // Get order status from the status badge
            const statusBadge = card.querySelector('.inline-flex.px-3.py-1');
            const orderStatus = statusBadge ? statusBadge.textContent.toLowerCase().trim() : '';
            
            // Check if order matches search term (book title only)
            const matchesSearch = !searchTerm || bookTitle.includes(searchTerm);
            
            // Check if order matches status filter
            const matchesStatus = !statusFilter || checkStatusMatch(orderStatus, statusFilter);

            if (matchesSearch && matchesStatus) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Show/hide empty state message when no results found
        const emptyState = document.querySelector('.bg-white.rounded-lg.shadow-sm.p-12.text-center');
        if (emptyState) {
            const hasNoOrders = emptyState.querySelector('h2')?.textContent.includes('ยังไม่มีประวัติการสั่งซื้อ');
            
            if (visibleCount === 0 && (searchTerm || statusFilter)) {
                // Show "no results found" state when filtering but no matches
                emptyState.style.display = 'block';
                const heading = emptyState.querySelector('h2');
                const description = emptyState.querySelector('p');
                if (heading) heading.textContent = 'ไม่พบผลลัพธ์ที่ค้นหา';
                if (description) description.textContent = 'ลองค้นหาด้วยชื่อหนังสือหรือสถานะที่แตกต่างกัน';
            } else if (visibleCount === 0 && !searchTerm && !statusFilter && hasNoOrders) {
                // Show original empty state when no orders exist
                emptyState.style.display = 'block';
            } else if (visibleCount > 0) {
                // Hide empty state when there are visible orders
                emptyState.style.display = 'none';
            }
        }
    }

    function checkStatusMatch(orderStatus, statusFilter) {
        // Map status filter values to Thai status text
        const statusMap = {
            'pending': ['รอดำเนินการ'],
            'processing': ['กำลังประมวลผล', 'กำลังเตรียมสินค้า'],
            'shipped': ['จัดส่งแล้ว', 'กำลังจัดส่ง'],
            'delivered': ['ส่งมอบแล้ว', 'จัดส่งสำเร็จ'],
            'cancelled': ['ยกเลิกแล้ว', 'ยกเลิก'],
            'paid': ['ชำระเงินแล้ว'],
            'unpaid': ['ยังไม่ชำระเงิน']
        };

        const statusTexts = statusMap[statusFilter];
        if (!statusTexts) return false;

        // Check if order status matches any of the mapped status texts
        return statusTexts.some(text => orderStatus.includes(text.toLowerCase()));
    }
});