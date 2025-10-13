let selectedFile = null;

document.addEventListener('DOMContentLoaded', function () {
    // Payment method selection
    const paymentRadios = document.querySelectorAll('.payment-method-radio');
    const paymentSections = document.querySelectorAll('.payment-section');

    paymentRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            // Update card styling
            document.querySelectorAll('.payment-method-card').forEach(card => {
                card.classList.remove('active');
                card.classList.remove('border-orange-500');
                card.classList.add('border-gray-200');
            });

            const selectedCard = this.closest('.payment-method-option').querySelector('.payment-method-card');
            selectedCard.classList.add('active');
            selectedCard.classList.remove('border-gray-200');
            selectedCard.classList.add('border-orange-500');

            // Show/hide payment sections
            paymentSections.forEach(section => {
                section.classList.add('hidden');
                section.classList.remove('active');
            });

            if (this.value === 'promptpay') {
                document.getElementById('qr-section').classList.remove('hidden');
                document.getElementById('qr-section').classList.add('active');
                document.querySelector('.mb-8:has(#file-drop-zone)').style.display = 'block';
            } else if (this.value === 'bank_transfer') {
                document.getElementById('bank-transfer-section').classList.remove('hidden');
                document.getElementById('bank-transfer-section').classList.add('active');
                document.querySelector('.mb-8:has(#file-drop-zone)').style.display = 'block';
            } else if (this.value === 'cash_on_delivery') {
                // Hide file upload section for cash on delivery
                document.querySelector('.mb-8:has(#file-drop-zone)').style.display = 'none';
            }

            updateSubmitButton();
        });
    });

    // File drop zone
    const dropZone = document.getElementById('file-drop-zone');

    dropZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        this.classList.add('border-orange-400', 'bg-orange-50');
    });

    dropZone.addEventListener('dragleave', function (e) {
        e.preventDefault();
        this.classList.remove('border-orange-400', 'bg-orange-50');
    });

    dropZone.addEventListener('drop', function (e) {
        e.preventDefault();
        this.classList.remove('border-orange-400', 'bg-orange-50');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect({ files: files });
        }
    });

    // Form submission
    document.getElementById('paymentForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const selectedMethod = document.querySelector('.payment-method-radio:checked');

        // Check if file is required (not required for cash_on_delivery)
        if (selectedMethod.value !== 'cash_on_delivery' && !selectedFile) {
            showError('กรุณาอัพโหลดหลักฐานการชำระเงิน');
            return;
        }

        // Simulate form submission
        const submitButton = document.getElementById('submit-payment');
        const originalText = submitButton.innerHTML;

        submitButton.disabled = true;
        submitButton.innerHTML = `
                    <span class="inline-flex items-center">
                        <svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        กำลังประมวลผล...
                    </span>
                `;

        setTimeout(() => {
            alert('ชำระเงินสำเร็จ! เราจะตรวจสอบการชำระเงินและยืนยันคำสั่งซื้อในไม่ช้า');
            window.location.href = '/order-confirmation';
        }, 2000);
    });

    // Cancel order
    const cancelButton = document.querySelector('[data-cancel-order]');
    if (cancelButton) {
        cancelButton.addEventListener('click', function () {
            if (confirm('คุณต้องการยกเลิกการสั่งซื้อนี้หรือไม่?')) {
                window.location.href = '/cart';
            }
        });
    }
});

function handleFileSelect(input) {
    const file = input.files[0];
    if (!file) return;

    // Validate file
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];

    if (file.size > maxSize) {
        showError('ขนาดไฟล์ต้องไม่เกิน 5MB');
        return;
    }

    if (!allowedTypes.includes(file.type)) {
        showError('รองรับเฉพาะไฟล์ JPG, PNG, และ PDF เท่านั้น');
        return;
    }

    selectedFile = file;
    showFilePreview(file);
    hideError();
    updateSubmitButton();
}

function showFilePreview(file) {
    const placeholder = document.getElementById('upload-placeholder');
    const preview = document.getElementById('file-preview');
    const previewContent = document.getElementById('preview-content');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');

    placeholder.classList.add('hidden');
    preview.classList.remove('hidden');

    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);

    if (file.type.startsWith('image/')) {
        const img = document.createElement('img');
        img.className = 'w-20 h-20 object-cover rounded-lg border';
        img.src = URL.createObjectURL(file);
        previewContent.innerHTML = '';
        previewContent.appendChild(img);
    } else {
        previewContent.innerHTML = `
                    <div class="w-20 h-20 bg-red-100 rounded-lg border flex items-center justify-center">
                        <svg class="w-8 h-8 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                        </svg>
                    </div>
                `;
    }
}

function removeFile() {
    selectedFile = null;
    document.getElementById('payment-proof').value = '';
    document.getElementById('upload-placeholder').classList.remove('hidden');
    document.getElementById('file-preview').classList.add('hidden');
    hideError();
    updateSubmitButton();
}

function showError(message) {
    const errorDiv = document.getElementById('upload-errors');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    document.getElementById('upload-errors').classList.add('hidden');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function updateSubmitButton() {
    const submitButton = document.getElementById('submit-payment');
    const hasFile = selectedFile !== null;
    const selectedMethod = document.querySelector('.payment-method-radio:checked');

    // For cash on delivery, no file upload is required
    if (selectedMethod && selectedMethod.value === 'cash_on_delivery') {
        submitButton.disabled = false;
        submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
    } else if (hasFile && selectedMethod) {
        submitButton.disabled = false;
        submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
        submitButton.disabled = true;
        submitButton.classList.add('opacity-50', 'cursor-not-allowed');
    }
}