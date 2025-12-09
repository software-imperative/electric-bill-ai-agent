// Utility Functions

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(date);
}

// Format datetime
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Format duration (seconds to readable format)
function formatDuration(seconds) {
    if (!seconds) return 'N/A';

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
        return `${minutes}m ${remainingSeconds}s`;
    }
    return `${seconds}s`;
}

// Get status badge HTML
function getStatusBadge(status) {
    const statusClass = `status-${status.toLowerCase()}`;
    return `<span class="status-badge ${statusClass}">${status}</span>`;
}

// Validate phone number
function validatePhone(phone) {
    const phoneRegex = /^[+]?[\d\s-()]+$/;
    return phoneRegex.test(phone);
}

// Validate email
function validateEmail(email) {
    if (!email) return true; // Email is optional
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Show loading state
function showLoading(element) {
    element.disabled = true;
    element.innerHTML = '<span class="loading"></span> Loading...';
}

// Hide loading state
function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

// Confirm action
function confirmAction(message) {
    return confirm(message);
}

// Get time of day greeting
function getTimeOfDay() {
    const hour = new Date().getHours();
    if (hour < 12) return 'morning';
    if (hour < 17) return 'afternoon';
    return 'evening';
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Calculate collection rate
function calculateCollectionRate(paid, total) {
    if (total === 0) return 0;
    return ((paid / total) * 100).toFixed(1);
}

// Export utilities
window.utils = {
    showToast,
    formatCurrency,
    formatDate,
    formatDateTime,
    formatDuration,
    getStatusBadge,
    validatePhone,
    validateEmail,
    showLoading,
    hideLoading,
    confirmAction,
    getTimeOfDay,
    debounce,
    calculateCollectionRate
};
