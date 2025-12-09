// Frontend Configuration
// This file can be updated during deployment to set the API URL
// For Netlify/Vercel: Set API_BASE_URL environment variable
// The API client will use window.API_BASE_URL if available, otherwise fallback to this

const CONFIG = {
    // API Base URL - Will be overridden by environment variable or window.API_BASE_URL
    API_BASE_URL: window.API_BASE_URL || 'http://localhost:8000'
};

// Make it globally available
window.CONFIG = CONFIG;

