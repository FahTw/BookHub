let currentOrderId = null;
let sortColumn = null;
let sortDirection = 'asc';

document.addEventListener('DOMContentLoaded', function () {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const dateFilter = document.getElementById('dateFilter');

    if (searchInput) {
        searchInput.addEventListener('input', filterOrders);
    }
    if (statusFilter) {
        statusFilter.addEventListener('change', filterOrders);
    }
    if (dateFilter) {
        dateFilter.addEventListener('change', filterOrders);
    }

    // Initialize
    updatePaginationInfo();
});

function filterOrders() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    const dateFilter = document.getElementById('dateFilter').value;

    const rows = document.querySelectorAll('#ordersTableBody tr');
    let visibleCount = 0;

    rows.forEach(row => {
        const orderText = row.textContent.toLowerCase();
        const orderStatus = row.dataset.status;

        const matchesSearch = !searchTerm || orderText.includes(searchTerm);
        const matchesStatus = !statusFilter || orderStatus === statusFilter;
        const matchesDate = !dateFilter || checkDateFilter(row, dateFilter);

        if (matchesSearch && matchesStatus && matchesDate) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    // Show/hide empty state
    const emptyState = document.getElementById('emptyState');
    const ordersTable = document.querySelector('.bg-white.rounded-lg.shadow-sm.overflow-hidden.border');

    if (visibleCount === 0) {
        emptyState.classList.remove('hidden');
        ordersTable.style.display = 'none';
    } else {
        emptyState.classList.add('hidden');
        ordersTable.style.display = 'block';
    }

    updatePaginationInfo(visibleCount);
}

function checkDateFilter(row, filter) {
    // Implement date filtering logic based on the filter value
    return true; // Simplified for now
}

function sortTable(column) {
    // Implement sorting functionality
    console.log('Sorting by:', column);
}

function viewOrder(orderId) {
    // Redirect to order detail page
    window.location.href = `/orderhistorydetail?id=${orderId}`;
}

function updateStatus(orderId) {
    currentOrderId = orderId;
    document.getElementById('modalOrderId').textContent = orderId;
    document.getElementById('statusModal').classList.remove('hidden');
}

function closeStatusModal() {
    document.getElementById('statusModal').classList.add('hidden');
    currentOrderId = null;
}

function saveStatusUpdate() {
    const newStatus = document.getElementById('newStatus').value;
    const note = document.getElementById('statusNote').value;

    // Here you would normally send the update to the server
    console.log('Updating order', currentOrderId, 'to status:', newStatus, 'with note:', note);

    // Update the UI
    const row = document.querySelector(`tr[data-order-id="${currentOrderId}"]`);
    if (row) {
        row.dataset.status = newStatus;
        const statusCell = row.querySelector('.px-2.inline-flex');
        if (statusCell) {
            statusCell.className = `px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusClasses(newStatus)}`;
            statusCell.textContent = getStatusText(newStatus);
        }
    }

    alert('อัปเดตสถานะเรียบร้อยแล้ว');
    closeStatusModal();
}

function getStatusClasses(status) {
    const classes = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'processing': 'bg-blue-100 text-blue-800',
        'shipped': 'bg-orange-100 text-orange-800',
        'delivered': 'bg-green-100 text-green-800',
        'cancelled': 'bg-red-100 text-red-800'
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
}

function getStatusText(status) {
    const texts = {
        'pending': 'รอดำเนินการ',
        'processing': 'กำลังประมวลผล',
        'shipped': 'กำลังจัดส่ง',
        'delivered': 'จัดส่งสำเร็จ',
        'cancelled': 'ยกเลิกแล้ว'
    };
    return texts[status] || 'ไม่ทราบสถานะ';
}

function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('statusFilter').value = '';
    document.getElementById('dateFilter').value = '';
    filterOrders();
}

function updatePaginationInfo(visibleCount = null) {
    const totalItems = document.getElementById('totalItems');
    const currentRange = document.getElementById('currentRange');

    if (visibleCount !== null) {
        totalItems.textContent = visibleCount;
        currentRange.textContent = visibleCount > 0 ? `1-${Math.min(5, visibleCount)}` : '0-0';
    }
}