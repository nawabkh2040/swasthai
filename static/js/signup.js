// Signup Page JavaScript
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fullName = document.getElementById('fullName').value.trim();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    const errorMsg = document.getElementById('errorMessage');
    const successMsg = document.getElementById('successMessage');
    const submitBtn = document.getElementById('submitBtn');
    
    // Clear previous messages
    errorMsg.className = '';
    errorMsg.textContent = '';
    successMsg.className = '';
    successMsg.textContent = '';
    
    // Validation
    if (password !== confirmPassword) {
        errorMsg.className = 'alert alert-danger';
        errorMsg.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Passwords do not match';
        return;
    }
    
    if (password.length < 6) {
        errorMsg.className = 'alert alert-danger';
        errorMsg.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Password must be at least 6 characters';
        return;
    }
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creating Account...';
    
    try {
        const response = await fetch('/api/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password,
                full_name: fullName
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save token
            localStorage.setItem('token', data.access_token);
            
            successMsg.className = 'alert alert-success';
            successMsg.innerHTML = '<i class="bi bi-check-circle me-2"></i>Account created successfully! Redirecting...';
            
            // Redirect to chat
            setTimeout(() => {
                window.location.href = '/chat';
            }, 1500);
        } else {
            // Get error message from response
            const errorMessage = data.error || data.detail || 'Signup failed. Please try again.';
            errorMsg.className = 'alert alert-danger';
            errorMsg.innerHTML = '<i class="bi bi-exclamation-circle me-2"></i>' + errorMessage;
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-person-plus me-2"></i>Create Account';
        }
    } catch (error) {
        console.error('Signup error:', error);
        errorMsg.className = 'alert alert-danger';
        errorMsg.innerHTML = '<i class="bi bi-wifi-off me-2"></i>Network error. Please check your connection.';
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-person-plus me-2"></i>Create Account';
    }
});

// Auto-resize username to lowercase
document.getElementById('username').addEventListener('input', (e) => {
    e.target.value = e.target.value.toLowerCase();
});
