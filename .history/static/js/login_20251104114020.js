// Login Page JavaScript
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    const errorMsg = document.getElementById('errorMessage');
    const submitBtn = document.getElementById('submitBtn');
    
    // Clear previous messages
    errorMsg.classList.remove('show');
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';
    
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
            
            // Redirect to chat
            window.location.href = '/chat';
        } else {
            errorMsg.textContent = data.detail || 'Login failed. Please check your credentials.';
            errorMsg.classList.add('show');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Login';
        }
    } catch (error) {
        console.error('Login error:', error);
        errorMsg.textContent = 'Network error. Please check your connection.';
        errorMsg.classList.add('show');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Login';
    }
});
