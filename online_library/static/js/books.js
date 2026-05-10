// ================= BOOK DETAILS =================
function goToDetails(id) {
    window.location.href = `/book/${id}/`;
}

// ================= BORROW BOOK =================
function borrowBook(id) {
    window.location.href = `/borrow/${id}/`;
}