// Frontend Configuration
// This file can be updated during deployment to set the API URL
// For Netlify/Vercel: Set API_BASE_URL environment variable
// The API client will use window.API_BASE_URL if available, otherwise fallback to this

const CONFIG = {
    // API Base URL - Production backend URL
    // Netlify env vars aren't available at runtime, so we set production URL here
    API_BASE_URL: window.API_BASE_URL || 'https://adani-bill-collection-api.onrender.com'
};

// Make it globally available
window.CONFIG = CONFIG;

