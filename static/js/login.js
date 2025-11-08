// Login Page JavaScript
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    const errorMsg = document.getElementById('errorMessage');
    const submitBtn = document.getElementById('submitBtn');
    
    // Clear previous messages
    errorMsg.className = '';
    errorMsg.textContent = '';
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Logging in...';
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save token
            localStorage.setItem('token', data.access_token);
            
            // Show success message
            errorMsg.className = 'alert alert-success';
            errorMsg.innerHTML = '<i class="bi bi-check-circle me-2"></i>Login successful! Redirecting...';
            
            // Redirect to chat
            setTimeout(() => {
                window.location.href = '/chat';
            }, 500);
        } else {
            // Get error message from response
            const errorMessage = data.error || data.detail || 'Login failed. Please check your credentials.';
            errorMsg.className = 'alert alert-danger';
            errorMsg.innerHTML = '<i class="bi bi-exclamation-circle me-2"></i>' + errorMessage;
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-box-arrow-in-right me-2"></i>Login';
        }
    } catch (error) {
        console.error('Login error:', error);
        errorMsg.className = 'alert alert-danger';
        errorMsg.innerHTML = '<i class="bi bi-wifi-off me-2"></i>Network error. Please check your connection.';
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-box-arrow-in-right me-2"></i>Login';
    }
});
