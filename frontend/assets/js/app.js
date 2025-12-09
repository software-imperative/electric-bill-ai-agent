// Main Application Logic

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    setupModals();
    setupForms();
    setupFilters();
    setupQuickActions();

    // Load initial dashboard
    dashboard.loadDashboard();
}

// Navigation
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const viewName = item.dataset.view;

            // Update active nav item
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Update active view
            views.forEach(view => view.classList.remove('active'));
            document.getElementById(`${viewName}-view`).classList.add('active');

            // Load view data
            loadViewData(viewName);
        });
    });
}

function loadViewData(viewName) {
    switch (viewName) {
        case 'dashboard':
            dashboard.loadDashboard();
            break;
        case 'bills':
            dashboard.loadBillsTable();
            break;
        case 'calls':
            dashboard.loadCallLogs();
            break;
        case 'analytics':
            dashboard.loadAnalytics();
            break;
    }
}

// Modals
function setupModals() {
    const modal = document.getElementById('addBillModal');
    const openButtons = [
        document.getElementById('addBillBtn'),
        document.getElementById('addBillBtnAlt')
    ];
    const closeButton = document.getElementById('closeModal');
    const cancelButton = document.getElementById('cancelBtn');

    openButtons.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', () => {
                modal.classList.add('active');
            });
        }
    });

    const closeModal = () => {
        modal.classList.remove('active');
        document.getElementById('addBillForm').reset();
    };

    closeButton.addEventListener('click', closeModal);
    cancelButton.addEventListener('click', closeModal);

    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Forms
function setupForms() {
    const form = document.getElementById('addBillForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form data
        const formData = {
            customer_name: document.getElementById('customerName').value,
            customer_phone: document.getElementById('customerPhone').value,
            customer_email: document.getElementById('customerEmail').value || null,
            consumer_number: document.getElementById('consumerNumber').value,
            bill_number: document.getElementById('billNumber').value,
            bill_amount: parseFloat(document.getElementById('billAmount').value),
            due_date: new Date(document.getElementById('dueDate').value).toISOString(),
            billing_period: document.getElementById('billingPeriod').value || null
        };

        // Validate
        if (!utils.validatePhone(formData.customer_phone)) {
            utils.showToast('Invalid phone number', 'error');
            return;
        }

        if (!utils.validateEmail(formData.customer_email)) {
            utils.showToast('Invalid email address', 'error');
            return;
        }

        try {
            await api.createBill(formData);
            utils.showToast('Bill created successfully!', 'success');

            // Close modal and refresh
            document.getElementById('addBillModal').classList.remove('active');
            form.reset();

            await dashboard.loadDashboard();
            await dashboard.loadBillsTable();

        } catch (error) {
            console.error('Error creating bill:', error);
            utils.showToast(error.message || 'Failed to create bill', 'error');
        }
    });
}

// Filters
function setupFilters() {
    const billStatusFilter = document.getElementById('billStatusFilter');
    const callStatusFilter = document.getElementById('callStatusFilter');

    if (billStatusFilter) {
        billStatusFilter.addEventListener('change', (e) => {
            dashboard.loadBillsTable(e.target.value);
        });
    }

    if (callStatusFilter) {
        callStatusFilter.addEventListener('change', (e) => {
            dashboard.loadCallLogs(e.target.value);
        });
    }
}

// Quick Actions
function setupQuickActions() {
    const refreshBtn = document.getElementById('refreshDashboard');
    const initiateCallsBtn = document.getElementById('initiateCallsBtn');
    const viewPendingBtn = document.getElementById('viewPendingBtn');

    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            dashboard.loadDashboard();
            utils.showToast('Dashboard refreshed', 'success');
        });
    }

    if (initiateCallsBtn) {
        initiateCallsBtn.addEventListener('click', async () => {
            if (!utils.confirmAction('Initiate calls for all pending bills?')) {
                return;
            }

            try {
                const response = await api.getPendingBills();
                const bills = response.bills || [];

                if (bills.length === 0) {
                    utils.showToast('No pending bills to call', 'info');
                    return;
                }

                utils.showToast(`Initiating calls for ${bills.length} bills...`, 'info');

                // Initiate calls for each bill (with delay to avoid overwhelming the system)
                for (let i = 0; i < Math.min(bills.length, 5); i++) {
                    await api.initiateCall(bills[i].id);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }

                utils.showToast('Calls initiated successfully!', 'success');
                await dashboard.loadDashboard();

            } catch (error) {
                console.error('Error initiating calls:', error);
                utils.showToast(error.message || 'Failed to initiate calls', 'error');
            }
        });
    }

    if (viewPendingBtn) {
        viewPendingBtn.addEventListener('click', () => {
            // Switch to bills view with pending filter
            document.querySelector('[data-view="bills"]').click();
            setTimeout(() => {
                document.getElementById('billStatusFilter').value = 'pending';
                dashboard.loadBillsTable('pending');
            }, 100);
        });
    }
}

// Auto-refresh dashboard every 30 seconds
setInterval(() => {
    const activeView = document.querySelector('.view.active');
    if (activeView && activeView.id === 'dashboard-view') {
        dashboard.loadDashboard();
    }
}, 30000);

// Check API health on load
api.healthCheck()
    .then(() => {
        console.log('✅ Backend API is healthy');
    })
    .catch((error) => {
        console.error('❌ Backend API is not responding:', error);
        utils.showToast('Warning: Backend API is not responding', 'warning');
    });
