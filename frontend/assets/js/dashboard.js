// Dashboard functionality

class Dashboard {
    constructor() {
        this.stats = {
            total: 0,
            pending: 0,
            paid: 0,
            overdue: 0
        };
    }

    async loadDashboard() {
        try {
            await Promise.all([
                this.loadStats(),
                this.loadRecentActivity(),
                this.loadOverdueBills()
            ]);
        } catch (error) {
            console.error('Error loading dashboard:', error);
            utils.showToast('Failed to load dashboard data', 'error');
        }
    }

    async loadStats() {
        try {
            const response = await api.getBills();
            const bills = response.bills || [];

            this.stats.total = bills.length;
            this.stats.pending = bills.filter(b => b.status === 'pending').length;
            this.stats.paid = bills.filter(b => b.status === 'paid').length;
            this.stats.overdue = bills.filter(b => b.status === 'overdue').length;

            this.updateStatsDisplay();
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    updateStatsDisplay() {
        document.getElementById('totalBills').textContent = this.stats.total;
        document.getElementById('pendingBills').textContent = this.stats.pending;
        document.getElementById('paidBills').textContent = this.stats.paid;

        const collectionRate = utils.calculateCollectionRate(this.stats.paid, this.stats.total);
        document.getElementById('collectionRate').textContent = `${collectionRate}%`;
    }

    async loadRecentActivity() {
        try {
            const callLogs = await api.getCallLogs({ limit: 5 });
            const container = document.getElementById('recentActivity');

            if (!callLogs || callLogs.length === 0) {
                container.innerHTML = '<p class="empty-state">No recent activity</p>';
                return;
            }

            container.innerHTML = callLogs.map(call => `
                <div class="activity-item">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <strong>${call.customer_phone}</strong>
                            ${utils.getStatusBadge(call.status)}
                        </div>
                        <small style="color: var(--text-muted);">
                            ${utils.formatDateTime(call.created_at)}
                        </small>
                    </div>
                    ${call.outcome ? `<small style="color: var(--text-secondary);">Outcome: ${call.outcome}</small>` : ''}
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading recent activity:', error);
        }
    }

    async loadOverdueBills() {
        try {
            const response = await api.getOverdueBills();
            const bills = response.bills || [];
            const container = document.getElementById('overdueBills');

            if (bills.length === 0) {
                container.innerHTML = '<p class="empty-state">No overdue bills</p>';
                return;
            }

            container.innerHTML = bills.slice(0, 5).map(bill => `
                <div class="bill-item">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <strong>${bill.customer_name}</strong>
                            <br>
                            <small style="color: var(--text-secondary);">${bill.bill_number}</small>
                        </div>
                        <div style="text-align: right;">
                            <strong style="color: var(--danger-color);">${utils.formatCurrency(bill.bill_amount)}</strong>
                            <br>
                            <small style="color: var(--text-muted);">Due: ${utils.formatDate(bill.due_date)}</small>
                        </div>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading overdue bills:', error);
        }
    }

    async loadBillsTable(status = '') {
        try {
            const params = status ? { status } : {};
            const response = await api.getBills(params);
            const bills = response.bills || [];
            const tbody = document.getElementById('billsTableBody');

            if (bills.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No bills found</td></tr>';
                return;
            }

            tbody.innerHTML = bills.map(bill => `
                <tr>
                    <td>${bill.bill_number}</td>
                    <td>${bill.customer_name}</td>
                    <td>${bill.customer_phone}</td>
                    <td>${utils.formatCurrency(bill.bill_amount)}</td>
                    <td>${utils.formatDate(bill.due_date)}</td>
                    <td>${utils.getStatusBadge(bill.status)}</td>
                    <td>
                        <div class="table-actions">
                            ${bill.status !== 'paid' ? `
                                <button class="action-btn call" onclick="dashboard.initiateCall(${bill.id})">
                                    📞 Call
                                </button>
                            ` : ''}
                            <button class="action-btn view" onclick="dashboard.viewBill(${bill.id})">
                                👁️ View
                            </button>
                            <button class="action-btn delete" onclick="dashboard.deleteBill(${bill.id})">
                                🗑️ Delete
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error loading bills:', error);
            utils.showToast('Failed to load bills', 'error');
        }
    }

    async loadCallLogs(status = '') {
        try {
            const params = status ? { status } : {};
            const callLogs = await api.getCallLogs(params);
            const tbody = document.getElementById('callsTableBody');

            if (!callLogs || callLogs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="empty-state">No call logs found</td></tr>';
                return;
            }

            tbody.innerHTML = callLogs.map(call => `
                <tr>
                    <td>${call.vapi_call_id || 'N/A'}</td>
                    <td>Bill #${call.bill_id}</td>
                    <td>${call.customer_phone}</td>
                    <td>${utils.getStatusBadge(call.status)}</td>
                    <td>${call.outcome ? utils.getStatusBadge(call.outcome) : 'N/A'}</td>
                    <td>${utils.formatDuration(call.duration)}</td>
                    <td>${utils.formatDateTime(call.created_at)}</td>
                    <td>
                        <button class="action-btn view" onclick="dashboard.viewCallDetails(${call.id})">
                            👁️ View
                        </button>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error loading call logs:', error);
            utils.showToast('Failed to load call logs', 'error');
        }
    }

    async loadAnalytics() {
        try {
            const [billsResponse, callLogs] = await Promise.all([
                api.getBills(),
                api.getCallLogs()
            ]);

            const bills = billsResponse.bills || [];
            const calls = callLogs || [];

            // Calculate metrics
            const totalCalls = calls.length;
            const successfulCalls = calls.filter(c => c.status === 'completed').length;
            const callSuccessRate = totalCalls > 0 ? ((successfulCalls / totalCalls) * 100).toFixed(1) : 0;

            const totalDuration = calls.reduce((sum, c) => sum + (c.duration || 0), 0);
            const avgDuration = totalCalls > 0 ? Math.round(totalDuration / totalCalls) : 0;

            const paidBills = bills.filter(b => b.status === 'paid').length;
            const calledBills = bills.filter(b => b.call_attempts > 0).length;
            const paymentConversion = calledBills > 0 ? ((paidBills / calledBills) * 100).toFixed(1) : 0;

            const totalCollection = bills
                .filter(b => b.status === 'paid')
                .reduce((sum, b) => sum + b.bill_amount, 0);

            // Update display
            document.getElementById('callSuccessRate').textContent = `${callSuccessRate}%`;
            document.getElementById('avgCallDuration').textContent = utils.formatDuration(avgDuration);
            document.getElementById('paymentConversion').textContent = `${paymentConversion}%`;
            document.getElementById('totalCollection').textContent = utils.formatCurrency(totalCollection);

        } catch (error) {
            console.error('Error loading analytics:', error);
            utils.showToast('Failed to load analytics', 'error');
        }
    }

    async initiateCall(billId) {
        if (!utils.confirmAction('Are you sure you want to initiate a call for this bill?')) {
            return;
        }

        try {
            const response = await api.initiateCall(billId);
            utils.showToast('Call initiated successfully!', 'success');
            await this.loadDashboard();
            await this.loadBillsTable();
        } catch (error) {
            console.error('Error initiating call:', error);
            utils.showToast(error.message || 'Failed to initiate call', 'error');
        }
    }

    async deleteBill(billId) {
        if (!utils.confirmAction('Are you sure you want to delete this bill?')) {
            return;
        }

        try {
            await api.deleteBill(billId);
            utils.showToast('Bill deleted successfully!', 'success');
            await this.loadDashboard();
            await this.loadBillsTable();
        } catch (error) {
            console.error('Error deleting bill:', error);
            utils.showToast(error.message || 'Failed to delete bill', 'error');
        }
    }

    viewBill(billId) {
        utils.showToast('View bill details - Feature coming soon!', 'info');
    }

    viewCallDetails(callId) {
        utils.showToast('View call details - Feature coming soon!', 'info');
    }
}

// Create global dashboard instance
const dashboard = new Dashboard();
