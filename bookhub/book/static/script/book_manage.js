function openCreateModal() {
    document.getElementById('createBookModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeCreateModal() {
    document.getElementById('createBookModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    document.getElementById('createBookForm').reset();
}

// Close modal when clicking outside
document.getElementById('createBookModal')?.addEventListener('click', function (e) {
    if (e.target === this) {
        closeCreateModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeCreateModal();
    }
});