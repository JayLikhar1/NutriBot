document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const formSections = document.querySelectorAll('.form-section');
    
    // Animate form sections on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    formSections.forEach(section => {
        // These properties are now set in CSS to avoid conflicts and ensure initial visibility
        // section.style.opacity = '0';
        // section.style.transform = 'translateY(20px)';
        // section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // Handle activity level selection
    const activityCards = document.querySelectorAll('.activity-card');
    activityCards.forEach(card => {
        const radio = card.querySelector('input[type="radio"]');
        card.addEventListener('click', () => {
            activityCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            radio.checked = true;
            
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            card.appendChild(ripple);
            
            const rect = card.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${event.clientX - rect.left - size/2}px`;
            ripple.style.top = `${event.clientY - rect.top - size/2}px`;
            
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Handle goal selection
    const goalCards = document.querySelectorAll('.goal-card');
    goalCards.forEach(card => {
        const radio = card.querySelector('input[type="radio"]');
        card.addEventListener('click', () => {
            goalCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            radio.checked = true;
            
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            card.appendChild(ripple);
            
            const rect = card.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${event.clientX - rect.left - size/2}px`;
            ripple.style.top = `${event.clientY - rect.top - size/2}px`;
            
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Handle diet preference (checkboxes) selection
    const checkboxLabels = document.querySelectorAll('.checkbox-label');
    checkboxLabels.forEach(label => {
        const checkbox = label.querySelector('input[type="checkbox"]');
        label.addEventListener('click', (e) => {
            // Prevent ripple on label click if it's already a click on the checkbox
            if (e.target === checkbox) return;

            // Toggle selected class
            label.classList.toggle('selected');
            checkbox.checked = !checkbox.checked;
            
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            label.appendChild(ripple);
            
            const rect = label.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${e.clientX - rect.left - size/2}px`;
            ripple.style.top = `${e.clientY - rect.top - size/2}px`;
            
            setTimeout(() => ripple.remove(), 600);
        });
        // Also handle change event for cases where checkbox is clicked directly
        checkbox.addEventListener('change', () => {
            label.classList.toggle('selected', checkbox.checked);
        });
    });

    // Form validation
    form.addEventListener('submit', (e) => {
        const age = document.getElementById('age').value;
        const gender = document.getElementById('gender').value;
        const weight = document.getElementById('weight').value;
        const height = document.getElementById('height').value;
        const activity = document.querySelector('input[name="activity_level"]:checked')?.value;
        const goal = document.querySelector('input[name="goal"]:checked')?.value;
        const dietCheckboxes = document.querySelectorAll('input[name="diet_type"]:checked');
        const diet = Array.from(dietCheckboxes).map(cb => cb.value);

        if (!age || !gender || !weight || !height || !activity || !goal || diet.length === 0) {
            e.preventDefault();
            showError('Please fill in all fields');
            return;
        }
        
        if (age < 15 || age > 100) {
            e.preventDefault();
            showError('Please enter a valid age between 15 and 100');
            return;
        }
        
        if (weight < 30 || weight > 300) {
            e.preventDefault();
            showError('Please enter a valid weight between 30 and 300 kg');
            return;
        }
        
        if (height < 100 || height > 250) {
            e.preventDefault();
            showError('Please enter a valid height between 100 and 250 cm');
            return;
        }
    });

    // Add input validation feedback with animations
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            validateInput(input);
        });
        
        input.addEventListener('blur', () => {
            validateInput(input);
        });

        // Add focus animation
        input.addEventListener('focus', () => {
            input.parentElement.style.transform = 'scale(1.02)';
            input.parentElement.style.transition = 'transform 0.3s ease';
        });

        input.addEventListener('blur', () => {
            input.parentElement.style.transform = 'scale(1)';
        });
    });

    // Add hover effect to radio options (now activity and goal cards)
    const interactiveCards = document.querySelectorAll('.activity-card, .goal-card');
    interactiveCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Add hover effect to checkbox labels (diet preferences)
    const interactiveLabels = document.querySelectorAll('.checkbox-label');
    interactiveLabels.forEach(label => {
        label.addEventListener('mouseenter', () => {
            label.style.transform = 'translateY(-2px)';
        });
        
        label.addEventListener('mouseleave', () => {
            label.style.transform = 'translateY(0)';
        });
    });
});

// Input validation function
function validateInput(input) {
    const value = input.value;
    const type = input.type;
    const id = input.id;
    
    // Remove existing error classes
    input.classList.remove('error');
    
    // Validate based on input type
    if (type === 'number') {
        if (id === 'age' && (value < 15 || value > 100)) {
            input.classList.add('error');
        } else if (id === 'weight' && (value < 30 || value > 300)) {
            input.classList.add('error');
        } else if (id === 'height' && (value < 100 || value > 250)) {
            input.classList.add('error');
        }
    }
}

// Show error message with animation
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.position = 'fixed';
    errorDiv.style.top = '20px';
    errorDiv.style.left = '50%';
    errorDiv.style.transform = 'translateX(-50%)';
    errorDiv.style.backgroundColor = '#ff6b6b';
    errorDiv.style.color = 'white';
    errorDiv.style.padding = '1rem 2rem';
    errorDiv.style.borderRadius = '8px';
    errorDiv.style.boxShadow = '0 4px 12px rgba(255, 107, 107, 0.3)';
    errorDiv.style.zIndex = '1000';
    errorDiv.style.animation = 'fadeIn 0.3s ease-out';

    document.body.appendChild(errorDiv);

    setTimeout(() => {
        errorDiv.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(errorDiv);
        }, 300);
    }, 3000);
}

// Add smooth scrolling for anchor links
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