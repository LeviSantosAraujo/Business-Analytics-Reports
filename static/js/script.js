// Business Analytics Dashboard - Custom JavaScript

// Global variables
let refreshInterval;
let isAutoRefresh = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize charts
    initializeCharts();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize animations
    initializeAnimations();
    
    // Check for auto-refresh preference
    checkAutoRefresh();
    
    console.log('Business Analytics Dashboard initialized');
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize charts (placeholder for future Chart.js implementations)
function initializeCharts() {
    // This can be extended with Chart.js implementations
    console.log('Charts initialized');
}

// Set up event listeners
function setupEventListeners() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Handle navigation highlighting
    handleNavigationHighlight();
    
    // Handle form submissions
    handleFormSubmissions();
    
    // Handle keyboard shortcuts
    handleKeyboardShortcuts();
}

// Initialize animations
function initializeAnimations() {
    // Add fade-in animation to elements
    const animatedElements = document.querySelectorAll('.fade-in-up');
    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add pulse animation to important elements
    const pulseElements = document.querySelectorAll('.pulse');
    pulseElements.forEach(element => {
        element.classList.add('pulse');
    });
}

// Handle navigation highlighting
function handleNavigationHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Handle form submissions
function handleFormSubmissions() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit(form);
        });
    });
}

// Handle individual form submission
function handleFormSubmit(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    // Show loading state
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    
    // Simulate API call
    setTimeout(() => {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
        showNotification('Form submitted successfully!', 'success');
    }, 2000);
}

// Handle keyboard shortcuts
function handleKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + R: Refresh data
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            refreshData();
        }
        
        // Ctrl/Cmd + E: Export data
        if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
            e.preventDefault();
            exportData();
        }
        
        // Escape: Close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

// Refresh data
function refreshData() {
    showLoadingModal();
    
    // Simulate data refresh
    setTimeout(() => {
        hideLoadingModal();
        showNotification('Data refreshed successfully!', 'success');
        updateLastRefreshTime();
    }, 1500);
}

// Export data
function exportData() {
    showLoadingModal();
    
    // Simulate export process
    setTimeout(() => {
        hideLoadingModal();
        showNotification('Export completed! Check your downloads folder.', 'success');
    }, 2000);
}

// Show loading modal
function showLoadingModal() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

// Hide loading modal
function hideLoadingModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    if (modal) {
        modal.hide();
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Update last refresh time
function updateLastRefreshTime() {
    const lastRefreshElement = document.getElementById('last-refresh');
    if (lastRefreshElement) {
        const now = new Date();
        lastRefreshElement.textContent = now.toLocaleString();
    }
}

// Check auto-refresh preference
function checkAutoRefresh() {
    const autoRefreshToggle = document.getElementById('auto-refresh-toggle');
    if (autoRefreshToggle) {
        autoRefreshToggle.addEventListener('change', function() {
            if (this.checked) {
                startAutoRefresh();
            } else {
                stopAutoRefresh();
            }
        });
    }
}

// Start auto-refresh
function startAutoRefresh() {
    if (!isAutoRefresh) {
        isAutoRefresh = true;
        refreshInterval = setInterval(() => {
            refreshData();
        }, 300000); // Refresh every 5 minutes
        showNotification('Auto-refresh enabled', 'info');
    }
}

// Stop auto-refresh
function stopAutoRefresh() {
    if (isAutoRefresh) {
        isAutoRefresh = false;
        clearInterval(refreshInterval);
        showNotification('Auto-refresh disabled', 'info');
    }
}

// Chart helper functions
function createChart(canvasId, type, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    
    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            ...options
        }
    });
}

// Update chart data
function updateChart(chart, newData) {
    if (!chart) return;
    
    chart.data = newData;
    chart.update();
}

// Format numbers
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) return 'N/A';
    
    if (typeof num === 'string') {
        num = parseFloat(num);
    }
    
    if (isNaN(num)) return 'N/A';
    
    return num.toLocaleString('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

// Format currency
function formatCurrency(num, currency = 'USD') {
    if (num === null || num === undefined) return 'N/A';
    
    if (typeof num === 'string') {
        num = parseFloat(num);
    }
    
    if (isNaN(num)) return 'N/A';
    
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(num);
}

// Format percentage
function formatPercentage(num, decimals = 2) {
    if (num === null || num === undefined) return 'N/A';
    
    if (typeof num === 'string') {
        num = parseFloat(num);
    }
    
    if (isNaN(num)) return 'N/A';
    
    return (num * 100).toFixed(decimals) + '%';
}

// Copy to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Failed to copy: ', err);
            showNotification('Failed to copy to clipboard', 'error');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            showNotification('Copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy: ', err);
            showNotification('Failed to copy to clipboard', 'error');
        }
        
        document.body.removeChild(textArea);
    }
}

// Download file
function downloadFile(data, filename, type = 'text/plain') {
    const blob = new Blob([data], { type: type });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate form
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
        
        // Email validation
        if (input.type === 'email' && input.value) {
            if (!validateEmail(input.value)) {
                input.classList.add('is-invalid');
                isValid = false;
            }
        }
    });
    
    return isValid;
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

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Handle window resize
window.addEventListener('resize', debounce(function() {
    // Re-render charts on resize
    const charts = Chart.instances;
    Object.values(charts).forEach(chart => {
        chart.resize();
    });
}, 250));

// Handle page visibility change
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden, pause auto-refresh
        if (isAutoRefresh) {
            stopAutoRefresh();
        }
    } else {
        // Page is visible, resume auto-refresh
        const autoRefreshToggle = document.getElementById('auto-refresh-toggle');
        if (autoRefreshToggle && autoRefreshToggle.checked) {
            startAutoRefresh();
        }
    }
});

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showNotification('An error occurred. Please try again.', 'error');
});

// Performance monitoring
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
});

// Service Worker registration (for PWA support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export functions for global access
window.BusinessAnalytics = {
    refreshData,
    exportData,
    showNotification,
    formatNumber,
    formatCurrency,
    formatPercentage,
    copyToClipboard,
    downloadFile,
    createChart,
    updateChart
};
