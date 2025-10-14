function openCreateModal() {
    document.getElementById('createBookModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeCreateModal() {
    document.getElementById('createBookModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    document.getElementById('createBookForm').reset();
}

function openCategoryModal() {
    document.getElementById('createCategoryModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeCategoryModal() {
    document.getElementById('createCategoryModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    document.getElementById('createCategoryForm').reset();
}

// Close modals when clicking outside
document.getElementById('createBookModal')?.addEventListener('click', function (e) {
    if (e.target === this) {
        closeCreateModal();
    }
});

document.getElementById('createCategoryModal')?.addEventListener('click', function (e) {
    if (e.target === this) {
        closeCategoryModal();
    }
});

// Close modals with Escape key
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeCreateModal();
        closeCategoryModal();
    }
});