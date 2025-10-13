// Order Status Management
function updateOrderStatus(newStatus) {
    if (confirm(`คุณต้องการเปลี่ยนสถานะเป็น "${newStatus}" หรือไม่?`)) {
        // Update status display
        const statusDisplay = document.querySelector('.bg-green-100');
        if (statusDisplay) {
            statusDisplay.textContent = newStatus;

            // Update colors based on status
            statusDisplay.className = 'px-3 py-1 rounded-full text-sm font-medium';
            if (newStatus.includes('รอดำเนินการ')) {
                statusDisplay.classList.add('bg-yellow-100', 'text-yellow-800');
            } else if (newStatus.includes('เตรียม')) {
                statusDisplay.classList.add('bg-blue-100', 'text-blue-800');
            } else if (newStatus.includes('จัดส่ง') && !newStatus.includes('สำเร็จ')) {
                statusDisplay.classList.add('bg-purple-100', 'text-purple-800');
            } else if (newStatus.includes('สำเร็จ')) {
                statusDisplay.classList.add('bg-green-100', 'text-green-800');
            } else if (newStatus.includes('ยกเลิก')) {
                statusDisplay.classList.add('bg-red-100', 'text-red-800');
            }
        }

        // Show success notification
        showNotification('อัปเดตสถานะสำเร็จ!', 'success');
    }
}

// Print order function
function printOrder() {
    window.print();
}

// Send email function
function sendEmail() {
    if (confirm('ส่งอีเมลการยืนยันคำสั่งซื้อให้ลูกค้าหรือไม่?')) {
        // Simulate sending email
        setTimeout(() => {
            showNotification('ส่งอีเมลสำเร็จแล้ว!', 'success');
        }, 1000);
    }
}

// View customer function
function viewCustomer() {
    // Simulate opening customer profile
    alert('เปิดข้อมูลลูกค้า:\n\nชื่อ: นายสมชาย ใจดี\nอีเมล: somchai@email.com\nโทรศัพท์: 098-765-4321\nสมาชิกตั้งแต่: 15 มกราคม 2568');
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg text-white transform transition-all duration-300 translate-x-full opacity-0`;

    if (type === 'success') {
        notification.classList.add('bg-green-500');
    } else if (type === 'error') {
        notification.classList.add('bg-red-500');
    } else {
        notification.classList.add('bg-blue-500');
    }

    notification.textContent = message;
    document.body.appendChild(notification);

    // Show notification
    setTimeout(() => {
        notification.classList.remove('translate-x-full', 'opacity-0');
    }, 100);

    // Hide notification
    setTimeout(() => {
        notification.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Breadcrumb hover effects
document.addEventListener('DOMContentLoaded', function () {
    const breadcrumbLinks = document.querySelectorAll('nav a');
    breadcrumbLinks.forEach(link => {
        link.addEventListener('mouseenter', function () {
            if (!this.classList.contains('text-orange-600')) {
                this.classList.add('text-orange-600');
            }
        });
        link.addEventListener('mouseleave', function () {
            if (this.textContent !== 'รายละเอียดคำสั่งซื้อ #1') {
                this.classList.remove('text-orange-600');
            }
        });
    });
});

// Responsive handling
function handleResize() {
    const width = window.innerWidth;
    const productDetails = document.querySelectorAll('.flex.flex-col.md\\:flex-row');

    productDetails.forEach(element => {
        if (width < 768) {
            element.classList.remove('md:flex-row');
            element.classList.add('flex-col');
        } else {
            element.classList.remove('flex-col');
            element.classList.add('md:flex-row');
        }
    });
}

window.addEventListener('resize', handleResize);
document.addEventListener('DOMContentLoaded', handleResize);