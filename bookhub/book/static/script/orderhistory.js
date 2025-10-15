document.addEventListener('DOMContentLoaded', function () {
    // ข้อความ search input เเละ ตัวเลือก status 
    const searchInput = document.querySelector('input[type="text"]');
    const statusSelect = document.querySelector('select');

    // เพิ่ม event
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const searchTerm = this.value.toLowerCase();
            const selectedStatus = statusSelect ? statusSelect.value : '';
            filterOrders(searchTerm, selectedStatus);
        });
    }

    // เพิ่ม event
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
            // ดึงข้อมูลหนังสือ
            const bookTitleElement = card.querySelector('h4.font-semibold.text-gray-900');
            const bookTitle = bookTitleElement ? bookTitleElement.textContent.toLowerCase() : '';
            
            // ดึงข้อมูลสถานะคำสั่งซื้อ
            const statusBadge = card.querySelector('.inline-flex.px-3.py-1');
            const orderStatus = statusBadge ? statusBadge.textContent.toLowerCase().trim() : '';
            
            // เช็คข้อมูลข้อมูลสั่งซื้อตรงกับชื่อหนังสือ
            const matchesSearch = !searchTerm || bookTitle.includes(searchTerm);
            
            // เช็คข้อมูลสถานะสั่งซื้อตรงกับสถานะค้นหา
            const matchesStatus = !statusFilter || checkStatusMatch(orderStatus, statusFilter);

            if (matchesSearch && matchesStatus) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // แสดงกับซ่อน
        const emptyState = document.querySelector('.bg-white.rounded-lg.shadow-sm.p-12.text-center');
        if (emptyState) {
            const hasNoOrders = emptyState.querySelector('h2')?.textContent.includes('ยังไม่มีประวัติการสั่งซื้อ');
            
            if (visibleCount === 0 && (searchTerm || statusFilter)) {
                // แสดง ไม่เจอผลลัพธ์
                emptyState.style.display = 'block';
                const heading = emptyState.querySelector('h2');
                const description = emptyState.querySelector('p');
                if (heading) heading.textContent = 'ไม่พบผลลัพธ์ที่ค้นหา';
                if (description) description.textContent = 'ลองค้นหาด้วยชื่อหนังสือหรือสถานะที่แตกต่างกัน';
            } else if (visibleCount === 0 && !searchTerm && !statusFilter && hasNoOrders) {
                // แสดงว่างเปล่า ถ้าไม่เจอคำสั่งซื้อ
                emptyState.style.display = 'block';
            } else if (visibleCount > 0) {
                // แสดงตตารางถ้ามีคำสั่งซื้อ
                emptyState.style.display = 'none';
            }
        }
    }

    function checkStatusMatch(orderStatus, statusFilter) {
        // map ค่า
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

        // เช็คถ้ามีสถานะตรงกับที่ map
        return statusTexts.some(text => orderStatus.includes(text.toLowerCase()));
    }
});