document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const form = document.querySelector('form.auth-form');
    const emailInput = document.getElementById('id_email');
    const passwordInput = document.getElementById('id_password1');
    const confirmPasswordInput = document.getElementById('id_password2');
    
    if (!form || !emailInput || !passwordInput || !confirmPasswordInput) return;
    
    // Email validation
    emailInput.addEventListener('blur', function() {
      const email = this.value.trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      
      if (email && !emailRegex.test(email)) {
        showError(this, 'Please enter a valid email address');
      } else {
        clearError(this);
      }
    });
    
    // Password strength feedback
    passwordInput.addEventListener('input', function() {
      const password = this.value;
      const strengthIndicator = getStrengthIndicator(password);
      
      // You could update a visual strength meter here
      if (password.length > 0) {
        this.classList.remove('error');
        if (strengthIndicator === 'weak') {
          this.classList.add('weak');
          this.classList.remove('medium', 'strong');
        } else if (strengthIndicator === 'medium') {
          this.classList.add('medium');
          this.classList.remove('weak', 'strong');
        } else {
          this.classList.add('strong');
          this.classList.remove('weak', 'medium');
        }
      } else {
        this.classList.remove('weak', 'medium', 'strong');
      }
    });
    
    // Confirm password validation
    confirmPasswordInput.addEventListener('input', function() {
      const password = passwordInput.value;
      const confirmPassword = this.value;
      
      if (confirmPassword && password !== confirmPassword) {
        showError(this, 'Passwords do not match');
      } else {
        clearError(this);
      }
    });
    
    // Helper functions
    function showError(element, message) {
      // Clear any existing error
      clearError(element);
      
      // Add error class
      element.classList.add('error');
      
      // Create error message
      const errorList = document.createElement('ul');
      errorList.className = 'errorlist';
      const errorItem = document.createElement('li');
      errorItem.textContent = message;
      errorList.appendChild(errorItem);
      
      // Insert after the input
      element.parentNode.insertBefore(errorList, element.nextSibling);
    }
    
    function clearError(element) {
      element.classList.remove('error');
      const parent = element.parentNode;
      const errorList = parent.querySelector('.errorlist');
      if (errorList) {
        parent.removeChild(errorList);
      }
    }
    
    function getStrengthIndicator(password) {
      if (!password) return '';
      
      // Basic password strength calculation
      let strength = 0;
      
      // Length check
      if (password.length >= 8) strength += 1;
      if (password.length >= 12) strength += 1;
      
      // Character variety checks
      if (/[A-Z]/.test(password)) strength += 1;
      if (/[a-z]/.test(password)) strength += 1;
      if (/[0-9]/.test(password)) strength += 1;
      if (/[^A-Za-z0-9]/.test(password)) strength += 1;
      
      if (strength < 3) return 'weak';
      if (strength < 5) return 'medium';
      return 'strong';
    }
  });