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
    
    // Validate username format (no @ symbol, only alphanumeric, underscore, hyphen)
    const usernameRegex = /^[a-zA-Z0-9_-]+$/;
    if (!usernameRegex.test(username)) {
        errorMsg.className = 'alert alert-danger';
        errorMsg.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Username can only contain letters, numbers, underscore and hyphen';
        return;
    }
    
    if (username.includes('@')) {
        errorMsg.className = 'alert alert-danger';
        errorMsg.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Please use a username, not an email address';
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
        
        console.log('Response status:', response.status);
        console.log('Response data:', data);
        
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
            let errorMessage = 'Signup failed. Please try again.';
            
            console.log('Error data.detail:', data.detail);
            console.log('Type of data.detail:', typeof data.detail);
            
            if (data.detail) {
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    // Handle validation errors from FastAPI
                    console.log('Array of errors:', data.detail);
                    const errors = [];
                    data.detail.forEach(err => {
                        console.log('Error item:', err);
                        if (err.msg) {
                            errors.push(err.msg);
                        } else if (err.message) {
                            errors.push(err.message);
                        } else if (typeof err === 'string') {
                            errors.push(err);
                        }
                    });
                    errorMessage = errors.length > 0 ? errors.join('. ') : 'Validation error occurred';
                } else if (typeof data.detail === 'object') {
                    // If it's an object, try to extract meaningful message
                    if (data.detail.msg) {
                        errorMessage = data.detail.msg;
                    } else if (data.detail.message) {
                        errorMessage = data.detail.message;
                    } else {
                        errorMessage = 'Invalid input. Please check your information.';
                    }
                }
            } else if (data.error) {
                errorMessage = data.error;
            }
            
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
