document.addEventListener('DOMContentLoaded', function () {
    // Payment method selection
    const paymentRadios = document.querySelectorAll('.payment-method-radio');
    const paymentSections = document.querySelectorAll('.payment-section');
    const fileUploadSection = document.getElementById('file-upload-section');
    const fileInput = document.getElementById('payment_slip');
    const placeholder = document.getElementById('preview-placeholder');
    const previewContainer = document.getElementById('preview-container');


    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (!file) {
                placeholder.style.display = 'block';
                previewContainer.innerHTML = '';
                return;
            }

            // ซ่อน placeholder
            if (placeholder) placeholder.style.display = 'none';
            previewContainer.innerHTML = '';

            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                img.className = "mx-auto mb-2 rounded-lg shadow-sm w-40 h-40 object-cover";
                previewContainer.appendChild(img);
            } else if (file.type === 'application/pdf') {
                previewContainer.innerHTML = `<p class="text-gray-500 text-sm">ไฟล์ PDF: ${file.name}</p>`;
            }

            updateSubmitButton(); // อัปเดตปุ่ม submit
        });
    }

    paymentRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            // Update card styling
            document.querySelectorAll('.payment-method-card').forEach(card => {
                card.classList.remove('active', 'border-orange-500');
                card.classList.add('border-gray-200');
            });

            const selectedCard = this.closest('.payment-method-option').querySelector('.payment-method-card');
            selectedCard.classList.add('active', 'border-orange-500');
            selectedCard.classList.remove('border-gray-200');

            // Show/hide payment sections
            paymentSections.forEach(section => {
                section.classList.add('hidden');
            });

            if (this.value === 'promptpay') {
                document.getElementById('qr-section').classList.remove('hidden');
                fileUploadSection.style.display = 'block';
            } else if (this.value === 'bank') {
                document.getElementById('bank-transfer-section').classList.remove('hidden');
                fileUploadSection.style.display = 'block';
            } else if (this.value === 'cash') {
                fileUploadSection.style.display = 'none';
            }

            updateSubmitButton();
        });
    });

    // File input change listener
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            updateSubmitButton();
        });
    }

    // Initialize submit button state
    updateSubmitButton();
});

function updateSubmitButton() {
    const submitButton = document.getElementById('submit-payment');
    const selectedMethod = document.querySelector('.payment-method-radio:checked');
    const fileInput = document.getElementById('payment_slip');
    const hasFile = fileInput && fileInput.files.length > 0;

    if (!selectedMethod) {
        submitButton.disabled = true;
        submitButton.classList.add('opacity-50', 'cursor-not-allowed');
        return;
    }

    // For cash on delivery, no file upload is required
    if (selectedMethod.value === 'cash') {
        submitButton.disabled = false;
        submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
    } else if (hasFile) {
        submitButton.disabled = false;
        submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
        submitButton.disabled = true;
        submitButton.classList.add('opacity-50', 'cursor-not-allowed');
    }
}