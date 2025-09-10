// Authentication functions
function login(username, password) {
    if (username === 'admin' && password === 'admin123') {
        localStorage.setItem('isLoggedIn', 'true');
        window.location.href = '/admin/dashboard';
        return true;
    }
    alert('Invalid credentials');
    return false;
}

function logout() {
    localStorage.removeItem('isLoggedIn');
    window.location.href = '/admin/login';
}

function checkAuth() {
    if (!localStorage.getItem('isLoggedIn')) {
        window.location.href = '/admin/login';
    }
}

// Dashboard functions
function showTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).style.display = 'block';
    
    // Add active class to clicked nav link
    event.target.classList.add('active');
}

// Form validation
function validateEventForm() {
    const name = document.getElementById('eventName').value;
    const date = document.getElementById('eventDate').value;
    const location = document.getElementById('eventLocation').value;
    
    if (!name || !date || !location) {
        alert('Please fill in all required fields');
        return false;
    }
    return true;
}

function validateDishForm() {
    const name = document.getElementById('dishName').value;
    const price = document.getElementById('dishPrice').value;
    
    if (!name || !price) {
        alert('Please fill in all required fields');
        return false;
    }
    return true;
}