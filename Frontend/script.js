// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
let parkingData = [];
let historyData = [];

// DOM Elements
const elements = {
    parkingGrid: document.getElementById('parkingGrid'),
    historyList: document.getElementById('historyList'),
    bookForm: document.getElementById('bookForm'),
    releaseForm: document.getElementById('releaseForm'),
    bookSlotId: document.getElementById('bookSlotId'),
    releaseSlotId: document.getElementById('releaseSlotId'),
    vehicleId: document.getElementById('vehicleId'),
    refreshBtn: document.getElementById('refreshBtn'),
    availableCount: document.getElementById('availableCount'),
    occupiedCount: document.getElementById('occupiedCount'),
    totalCount: document.getElementById('totalCount'),
    toast: document.getElementById('toast'),
    toastIcon: document.getElementById('toastIcon'),
    toastMessage: document.getElementById('toastMessage'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    tabButtons: document.querySelectorAll('.tab-button'),
    tabContents: document.querySelectorAll('.tab-content')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadParkingStatus();
    loadHistory();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadParkingStatus();
        loadHistory();
    }, 30000);
});

// Event Listeners
function initializeEventListeners() {
    // Tab switching
    elements.tabButtons.forEach(button => {
        button.addEventListener('click', () => switchTab(button.dataset.tab));
    });

    // Form submissions
    elements.bookForm.addEventListener('submit', handleBooking);
    elements.releaseForm.addEventListener('submit', handleRelease);

    // Refresh button
    elements.refreshBtn.addEventListener('click', () => {
        loadParkingStatus();
        loadHistory();
        showToast('Data refreshed', 'success', '🔄');
    });
}

// Tab Switching
function switchTab(tabName) {
    elements.tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    elements.tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
}

// API Functions
async function fetchAPI(endpoint, options = {}) {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        showToast(error.message || 'Network error occurred', 'error', '❌');
        throw error;
    } finally {
        showLoading(false);
    }
}

// Load Parking Status
async function loadParkingStatus() {
    try {
        const data = await fetchAPI('/parking/status');
        
        if (data.success) {
            parkingData = data.slots;
            updateParkingGrid(data.slots);
            updateStats(data.available_count, data.total_count);
            updateSlotDropdowns(data.slots);
        }
    } catch (error) {
        console.error('Failed to load parking status:', error);
    }
}

// Update Parking Grid
function updateParkingGrid(slots) {
    if (!slots || slots.length === 0) {
        elements.parkingGrid.innerHTML = '<p class="empty-history">No parking slots available</p>';
        return;
    }

    elements.parkingGrid.innerHTML = slots.map(slot => {
        const isAvailable = slot.status === 'available';
        const statusClass = isAvailable ? 'available' : 'occupied';
        const statusText = isAvailable ? 'Available' : 'Occupied';
        const vehicleInfo = slot.vehicle_id || 'No vehicle';
        const timeInfo = slot.booked_at ? formatDateTime(slot.booked_at) : '';

        return `
            <div class="parking-slot ${statusClass}" data-slot-id="${slot.slot_id}">
                <div class="slot-header">
                    <div class="slot-id">${slot.slot_id}</div>
                    <span class="slot-status ${statusClass}">${statusText}</span>
                </div>
                <div class="slot-details">
                    ${!isAvailable ? `
                        <div class="slot-info">
                            <div class="slot-vehicle">🚗 ${vehicleInfo}</div>
                        </div>
                        ${timeInfo ? `<div class="slot-time">⏰ ${timeInfo}</div>` : ''}
                    ` : `
                        <div class="slot-info" style="color: var(--success-color);">
                            ✓ Ready to book
                        </div>
                    `}
                </div>
            </div>
        `;
    }).join('');
}

// Update Statistics
function updateStats(available, total) {
    const occupied = total - available;
    
    elements.availableCount.textContent = available;
    elements.occupiedCount.textContent = occupied;
    elements.totalCount.textContent = total;

    // Animate numbers
    animateValue(elements.availableCount, 0, available, 500);
    animateValue(elements.occupiedCount, 0, occupied, 500);
}

// Update Slot Dropdowns
function updateSlotDropdowns(slots) {
    // Update book dropdown (available slots)
    const availableSlots = slots.filter(slot => slot.status === 'available');
    elements.bookSlotId.innerHTML = '<option value="">Select a slot</option>' +
        availableSlots.map(slot => `<option value="${slot.slot_id}">${slot.slot_id}</option>`).join('');

    // Update release dropdown (occupied slots)
    const occupiedSlots = slots.filter(slot => slot.status === 'occupied');
    elements.releaseSlotId.innerHTML = '<option value="">Select a slot</option>' +
        occupiedSlots.map(slot => `<option value="${slot.slot_id}">${slot.slot_id} - ${slot.vehicle_id}</option>`).join('');
}

// Handle Booking
async function handleBooking(e) {
    e.preventDefault();

    const slotId = elements.bookSlotId.value.trim();
    const vehicleId = elements.vehicleId.value.trim();

    if (!slotId || !vehicleId) {
        showToast('Please fill in all fields', 'warning', '⚠️');
        return;
    }

    try {
        const data = await fetchAPI('/parking/book', {
            method: 'POST',
            body: JSON.stringify({ slot_id: slotId, vehicle_id: vehicleId })
        });

        if (data.success) {
            showToast(data.message, 'success', '✅');
            elements.bookForm.reset();
            await loadParkingStatus();
            await loadHistory();
        }
    } catch (error) {
        // Error already handled in fetchAPI
    }
}

// Handle Release
async function handleRelease(e) {
    e.preventDefault();

    const slotId = elements.releaseSlotId.value.trim();

    if (!slotId) {
        showToast('Please select a slot', 'warning', '⚠️');
        return;
    }

    try {
        const data = await fetchAPI('/parking/release', {
            method: 'POST',
            body: JSON.stringify({ slot_id: slotId })
        });

        if (data.success) {
            showToast(data.message, 'success', '✅');
            elements.releaseForm.reset();
            await loadParkingStatus();
            await loadHistory();
        }
    } catch (error) {
        // Error already handled in fetchAPI
    }
}

// Load History
async function loadHistory() {
    try {
        const data = await fetchAPI('/parking/history');

        if (data.success) {
            historyData = data.history;
            updateHistoryList(data.history);
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// Update History List
function updateHistoryList(history) {
    if (!history || history.length === 0) {
        elements.historyList.innerHTML = '<p class="empty-history">No recent activity</p>';
        return;
    }

    // Reverse to show most recent first
    const reversedHistory = [...history].reverse();

    elements.historyList.innerHTML = reversedHistory.map(item => {
        const isBook = item.action === 'book';
        const icon = isBook ? '🅿️' : '🚪';
        const actionText = isBook ? 'Booked' : 'Released';
        const actionClass = isBook ? 'book' : 'release';

        return `
            <div class="history-item">
                <div class="history-icon ${actionClass}">${icon}</div>
                <div class="history-content">
                    <div class="history-details">
                        <div class="history-action">${actionText} - Slot ${item.slot_id}</div>
                        <div class="history-info">Vehicle: ${item.vehicle_id || 'N/A'}</div>
                    </div>
                    <div class="history-time">${formatDateTime(item.timestamp)}</div>
                </div>
            </div>
        `;
    }).join('');
}

// Utility Functions
function formatDateTime(isoString) {
    if (!isoString) return '';
    
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showToast(message, type = 'success', icon = '✅') {
    elements.toastIcon.textContent = icon;
    elements.toastMessage.textContent = message;
    elements.toast.className = `toast ${type} show`;

    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 4000);
}

function showLoading(show) {
    if (show) {
        elements.loadingOverlay.classList.add('show');
    } else {
        elements.loadingOverlay.classList.remove('show');
    }
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 16);
}

// Error Handling
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    showToast('An unexpected error occurred', 'error', '❌');
});
