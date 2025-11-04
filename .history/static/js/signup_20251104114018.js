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
    errorMsg.classList.remove('show');
    successMsg.classList.remove('show');
    
    // Validation
    if (password !== confirmPassword) {
        errorMsg.textContent = 'Passwords do not match';
        errorMsg.classList.add('show');
        return;
    }
    
    if (password.length < 6) {
        errorMsg.textContent = 'Password must be at least 6 characters';
        errorMsg.classList.add('show');
        return;
    }
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating Account...';
    
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
            
            successMsg.textContent = 'Account created successfully! Redirecting...';
            successMsg.classList.add('show');
            
            // Redirect to chat
            setTimeout(() => {
                window.location.href = '/chat';
            }, 1500);
        } else {
            errorMsg.textContent = data.detail || 'Signup failed. Please try again.';
            errorMsg.classList.add('show');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Account';
        }
    } catch (error) {
        console.error('Signup error:', error);
        errorMsg.textContent = 'Network error. Please check your connection.';
        errorMsg.classList.add('show');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create Account';
    }
});

// Auto-resize username to lowercase
document.getElementById('username').addEventListener('input', (e) => {
    e.target.value = e.target.value.toLowerCase();
});
