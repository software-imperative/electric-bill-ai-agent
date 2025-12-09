// API Base URL - Uses environment variable, config.js, or defaults to localhost for development
const API_BASE_URL = window.API_BASE_URL || (window.CONFIG && window.CONFIG.API_BASE_URL) || 'http://localhost:8000';

// API Client
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Bills API
    async getBills(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/bills?${queryString}`);
    }

    async getBill(billId) {
        return this.request(`/api/bills/${billId}`);
    }

    async createBill(billData) {
        return this.request('/api/bills/', {
            method: 'POST',
            body: JSON.stringify(billData)
        });
    }

    async updateBill(billId, billData) {
        return this.request(`/api/bills/${billId}`, {
            method: 'PUT',
            body: JSON.stringify(billData)
        });
    }

    async deleteBill(billId) {
        return this.request(`/api/bills/${billId}`, {
            method: 'DELETE'
        });
    }

    async initiateCall(billId) {
        return this.request(`/api/bills/${billId}/call`, {
            method: 'POST'
        });
    }

    async getPendingBills() {
        return this.request('/api/bills/pending/list');
    }

    async getOverdueBills() {
        return this.request('/api/bills/overdue/list');
    }

    // Calls API
    async getCallLogs(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/calls?${queryString}`);
    }

    async getCallLog(callLogId) {
        return this.request(`/api/calls/${callLogId}`);
    }

    // Payments API
    async getPayment(paymentId) {
        return this.request(`/api/payments/${paymentId}`);
    }

    async getPaymentByBill(billId) {
        return this.request(`/api/payments/bill/${billId}`);
    }

    // Health Check
    async healthCheck() {
        return this.request('/health');
    }
}

// Create global API instance
const api = new APIClient(API_BASE_URL);
