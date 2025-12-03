// Mobile toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.getElementById('mobileToggle');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            const sidebars = document.querySelectorAll('.sidebar');
            sidebars.forEach(sidebar => {
                sidebar.classList.toggle('active');
            });
        });
    }

    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.parentElement.remove();
                }
            }, 300);
        }, 5000);
    });

    // Login form loading indicator
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            const loginText = document.getElementById('login-text');
            const loginLoading = document.getElementById('login-loading');
            
            if (loginText && loginLoading) {
                loginText.style.display = 'none';
                loginLoading.style.display = 'inline-block';
            }
        });
    }

    // Navigation active states
    const navLinks = document.querySelectorAll('.nav-links li');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

// Toast functionality
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = 'toast';
    
    if (type === 'error') {
        toast.style.backgroundColor = 'var(--danger)';
    } else if (type === 'warning') {
        toast.style.backgroundColor = 'var(--warning)';
    } else {
        toast.style.backgroundColor = 'var(--primary)';
    }
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Filter functionality
function applyFilters() {
    const statusFilter = document.getElementById('filter-status');
    const priorityFilter = document.getElementById('filter-priority');
    
    if (!statusFilter || !priorityFilter) return;
    
    const statusValue = statusFilter.value;
    const priorityValue = priorityFilter.value;
    
    const rows = document.querySelectorAll('tbody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        const statusCell = row.querySelector('.status');
        const priorityCell = row.querySelector('.priority');
        
        let statusMatch = !statusValue || (statusCell && statusCell.classList.contains(statusValue));
        let priorityMatch = !priorityValue || (priorityCell && priorityCell.classList.contains(priorityValue));
        
        if (statusMatch && priorityMatch) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    showToast(`Mostrando ${visibleCount} tickets filtrados`);
}

// Search functionality
function searchTickets(tableId) {
    const searchInput = document.getElementById(`search-${tableId}-tickets`);
    if (!searchInput) return;
    
    const searchTerm = searchInput.value.toLowerCase();
    const table = document.getElementById(`${tableId}-tickets-table`);
    if (!table) return;
    
    const rows = table.getElementsByTagName('tr');
    let foundCount = 0;
    
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < cells.length; j++) {
            const cellText = cells[j].textContent || cells[j].innerText;
            if (cellText.toLowerCase().indexOf(searchTerm) > -1) {
                found = true;
                break;
            }
        }
        
        if (found) {
            rows[i].style.display = '';
            foundCount++;
        } else {
            rows[i].style.display = 'none';
        }
    }
    
    if (searchTerm) {
        showToast(`Encontrados ${foundCount} tickets`);
    }
}

// Modal functionality
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});

// Theme functionality
function applyTheme(theme) {
    const body = document.body;
    body.classList.remove('theme-light', 'theme-dark');
    
    if (theme === 'light') {
        body.classList.add('theme-light');
    } else {
        body.classList.add('theme-dark');
    }
}