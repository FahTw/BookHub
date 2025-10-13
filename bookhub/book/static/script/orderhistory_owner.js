document.addEventListener('DOMContentLoaded', function () {
    // Get search input and status select elements
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');

    // Add event listener for search input
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const searchTerm = this.value.toLowerCase();
            const selectedStatus = statusFilter ? statusFilter.value : '';
            filterOrders(searchTerm, selectedStatus);
        });
    }

    // Add event listener for status filter
    if (statusFilter) {
        statusFilter.addEventListener('change', function () {
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            const selectedStatus = this.value;
            filterOrders(searchTerm, selectedStatus);
        });
    }
});

function filterOrders(searchTerm, statusFilter) {
    const rows = document.querySelectorAll('#ordersTableBody tr');
    let visibleCount = 0;

    rows.forEach(row => {
        // Get order data from data attributes
        const bookTitle = row.dataset.bookTitle ? row.dataset.bookTitle.toLowerCase() : '';
        const customerName = row.dataset.customerName ? row.dataset.customerName.toLowerCase() : '';
        const orderId = row.dataset.orderId ? row.dataset.orderId.toLowerCase() : '';
        const orderStatus = row.dataset.status;

        // Check if order matches search term (search in book title, customer name, or order ID)
        const matchesSearch = !searchTerm || 
            bookTitle.includes(searchTerm) || 
            customerName.includes(searchTerm) || 
            orderId.includes(searchTerm);

        // Check if order matches status filter
        const matchesStatus = !statusFilter || orderStatus === statusFilter;

        if (matchesSearch && matchesStatus) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    // Show/hide empty state
    const ordersTable = document.querySelector('.bg-white.rounded-lg.shadow-sm.overflow-hidden.border');
    const emptyState = document.querySelector('.bg-white.rounded-lg.shadow-sm.p-12.text-center');

    if (visibleCount === 0 && (searchTerm || statusFilter)) {
        // Show "no results found" state when filtering but no matches
        if (ordersTable) ordersTable.style.display = 'none';
        if (emptyState) {
            emptyState.style.display = 'block';
            const heading = emptyState.querySelector('h2');
            const description = emptyState.querySelector('p');
            if (heading) heading.textContent = 'ไม่พบผลลัพธ์ที่ค้นหา';
            if (description) description.textContent = 'ลองค้นหาด้วยชื่อหนังสือ ชื่อลูกค้า หมายเลขคำสั่งซื้อ หรือสถานะที่แตกต่างกัน';
        }
    } else if (visibleCount > 0) {
        // Show table when there are visible orders
        if (ordersTable) ordersTable.style.display = 'block';
        if (emptyState) emptyState.style.display = 'none';
    } else if (visibleCount === 0 && !searchTerm && !statusFilter) {
        // Show original empty state when no orders exist (no filters applied)
        if (ordersTable) ordersTable.style.display = 'none';
        if (emptyState) {
            emptyState.style.display = 'block';
            const heading = emptyState.querySelector('h2');
            const description = emptyState.querySelector('p');
            if (heading) heading.textContent = 'ยังไม่มีคำสั่งซื้อ';
            if (description) description.textContent = 'เมื่อมีลูกค้าสั่งซื้อหนังสือ คำสั่งซื้อจะแสดงที่นี่';
        }
    }
}