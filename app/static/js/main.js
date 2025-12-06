// Main JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Format currency to display in EGP (Egyptian Pound)
function formatCurrency(value) {
    return new Intl.NumberFormat('ar-EG', {
        style: 'currency',
        currency: 'EGP'
    }).format(value);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(dateString).toLocaleDateString('ar-SA', options);
}

// Validate time slot selection
function validateTimeSlot(startTime, endTime) {
    if (!startTime || !endTime) {
        return false;
    }
    
    const [startHour, startMin] = startTime.split(':').map(Number);
    const [endHour, endMin] = endTime.split(':').map(Number);
    
    const startMinutes = startHour * 60 + startMin;
    const endMinutes = endHour * 60 + endMin;
    
    return endMinutes > startMinutes;
}

// Format time
function formatTime(timeString) {
    if (!timeString) return '';
    const [hours, minutes] = timeString.split(':');
    return `${hours}:${minutes}`;
}

// Show loading spinner
function showSpinner(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border spinner-small';
    spinner.role = 'status';
    element.appendChild(spinner);
}

// Clear spinner
function clearSpinner(element) {
    const spinner = element.querySelector('.spinner-border');
    if (spinner) {
        spinner.remove();
    }
}

// Confirm action
function confirmAction(message) {
    return confirm(message);
}

// Convert time format
function convertTo12Hour(time) {
    if (!time) return '';
    const [hours, minutes] = time.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'م' : 'ص';
    const hour12 = hour % 12 || 12;
    return `${hour12}:${minutes} ${ampm}`;
}

// Calculate booking duration in hours
function getBookingDuration(startTime, endTime) {
    const [startHour, startMin] = startTime.split(':').map(Number);
    const [endHour, endMin] = endTime.split(':').map(Number);
    
    const startMinutes = startHour * 60 + startMin;
    const endMinutes = endHour * 60 + endMin;
    
    const duration = endMinutes - startMinutes;
    return duration / 60;
}

// Calculate price based on duration and rate
function calculatePrice(duration, ratePerHour) {
    return (duration * ratePerHour).toFixed(2);
}

// Export table to CSV
function exportTableToCSV(filename) {
    const csv = [];
    const rows = document.querySelectorAll('table tbody tr');
    
    // Get headers
    const headers = [];
    document.querySelectorAll('table thead th').forEach(th => {
        headers.push(th.textContent.trim());
    });
    csv.push(headers.join(','));
    
    // Get rows
    rows.forEach(row => {
        const cols = [];
        row.querySelectorAll('td').forEach(td => {
            cols.push(`"${td.textContent.trim()}"`);
        });
        csv.push(cols.join(','));
    });
    
    // Download
    downloadCSV(csv.join('\n'), filename);
}

// Download CSV
function downloadCSV(csv, filename) {
    const link = document.createElement('a');
    link.href = 'data:text/csv;charset=utf-8,%EF%BB%BF' + encodeURIComponent(csv);
    link.download = filename;
    link.click();
}

// Get element's computed style
function getElementStyles(element) {
    return window.getComputedStyle(element);
}

// Smooth scroll to element
function smoothScroll(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Debounce function for search
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

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Get query parameters
function getQueryParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Check if localStorage is available
function isLocalStorageAvailable() {
    try {
        const test = '__local-storage-test__';
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
    } catch(e) {
        return false;
    }
}

// Navigate calendar month
function navigateCalendar(button, direction) {
    const container = button.closest('.hall-calendar');
    if (!container) {
        console.error('Calendar container not found');
        return;
    }
    
    const hallId = container.dataset.hallId;
    let year = parseInt(container.dataset.year);
    let month = parseInt(container.dataset.month);
    
    if (!hallId || !year || !month) {
        console.error('Missing calendar data:', { hallId, year, month });
        return;
    }
    
    // Calculate new month and year
    month += direction;
    if (month < 1) {
        month = 12;
        year -= 1;
    } else if (month > 12) {
        month = 1;
        year += 1;
    }
    
    // Disable button during loading
    button.disabled = true;
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    // Load the new month
    fetch(`/halls/${hallId}/calendar?year=${year}&month=${month}`)
        .then(r => {
            if (!r.ok) throw new Error('Network response was not ok');
            return r.text();
        })
        .then(html => {
            // Replace the container with new HTML
            container.outerHTML = html;
        })
        .catch(err => {
            console.error('Error loading calendar:', err);
            alert('حدث خطأ في تحميل التقويم');
            button.disabled = false;
            button.innerHTML = originalHTML;
        });
}

// Open hall calendar in global modal and navigate to booking on day click
function openHallCalendar(hallId) {
    const container = document.getElementById('globalCalendarContainer');
    if (!container) {
        alert('تعذر فتح التقويم - المودال غير موجود');
        return;
    }
    container.innerHTML = '<div class="text-center p-4">جاري تحميل التقويم...</div>';
    fetch(`/halls/${hallId}/calendar`)
        .then(r => r.text())
        .then(html => {
            container.innerHTML = html;
            const modalEl = document.getElementById('globalCalendarModal');
            const modal = new bootstrap.Modal(modalEl);
            modal.show();

            // Delegate clicks on available days
            container.addEventListener('click', function onCalClick(e){
                const td = e.target.closest('.calendar-day');
                if (!td) return;
                if (td.classList.contains('booked')) return;
                const date = td.getAttribute('data-date');
                if (date) {
                    // Navigate to booking add page with hall_id and date
                    window.location.href = `/bookings/add?hall_id=${hallId}&date=${date}`;
                }
            });
        })
        .catch(err => {
            console.error(err);
            container.innerHTML = '<div class="text-danger p-3">تعذر تحميل التقويم</div>';
        });
}

// Save to localStorage
function saveToStorage(key, value) {
    if (isLocalStorageAvailable()) {
        localStorage.setItem(key, JSON.stringify(value));
    }
}

// Get from localStorage
function getFromStorage(key) {
    if (isLocalStorageAvailable()) {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    }
    return null;
}

// Remove from localStorage
function removeFromStorage(key) {
    if (isLocalStorageAvailable()) {
        localStorage.removeItem(key);
    }
}
