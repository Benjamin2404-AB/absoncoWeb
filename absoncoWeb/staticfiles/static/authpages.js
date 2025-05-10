// static/js/auth-pages.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');
    if (!form) return;
  
    // Handle form submission to prevent double submits
    form.addEventListener('submit', function(e) {
      const submitButton = form.querySelector('.auth-button');
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';
        setTimeout(() => {
          submitButton.disabled = false;
          submitButton.textContent = 'Sign Up';
        }, 3000);
      }
    });
  
    // Add animation to social buttons
    const socialButtons = document.querySelectorAll('.social-button');
    socialButtons.forEach(button => {
      button.addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
          this.style.transform = 'scale(1)';
        }, 150);
      });
    });
  
    // Ensure password requirements remain visible on error
    const passwordField = document.getElementById('id_password1');
    const passwordErrors = document.getElementById('password1-error');
    if (passwordField && passwordErrors) {
      passwordField.addEventListener('input', function() {
        const requirements = document.querySelector('.password-requirements.compact');
        if (this.classList.contains('error')) {
          requirements.style.opacity = '1';
          requirements.style.color = '#dc3545'; // Highlight in red on error
        } else {
          requirements.style.opacity = '0.7';
          requirements.style.color = '#6b7280';
        }
      });
    }
  });