document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('diet-form');
    const chatMessages = document.getElementById('chat-messages');
    const loadingOverlay = document.getElementById('loading-overlay');
    const notificationArea = document.getElementById('notification-area');
    let currentStep = 1;
    const totalSteps = 7;

    // Initialize the first step
    showStep(1);

    // Handle next button clicks
    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', () => {
            if (validateCurrentStep()) {
                currentStep++;
                showStep(currentStep);
                addBotMessage(getStepMessage(currentStep));
            }
        });
    });

    // Handle previous button clicks
    document.querySelectorAll('.btn-prev').forEach(button => {
        button.addEventListener('click', () => {
            currentStep--;
            showStep(currentStep);
        });
    });

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validateCurrentStep()) {
            showNotification('Please fill in all required fields correctly.', 'error');
            return;
        }

        loadingOverlay.classList.add('active');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Convert number fields
        data.age = parseInt(data.age);
        data.weight = parseFloat(data.weight);
        data.height = parseFloat(data.height);
        if (data.target_weight) {
            data.target_weight = parseFloat(data.target_weight);
        }

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                const result = await response.json();
                showNotification('Diet plan generated successfully! Redirecting...', 'success', 2000);
                window.location.href = result.redirect_url || '/result';
            } else {
                const errorData = await response.json();
                showNotification(`Failed to generate diet plan: ${errorData.error || 'Unknown error'}`, 'error', 5000);
            }
        } catch (error) {
            console.error('Form submission error:', error);
            showNotification('An unexpected error occurred. Please try again later.', 'error', 5000);
            // Fallback to traditional form submission if AJAX fails
            form.submit();
        } finally {
            loadingOverlay.classList.remove('active');
        }
    });

    // Helper Functions
    function showStep(step) {
        document.querySelectorAll('.form-step').forEach(el => {
            el.classList.remove('active');
        });
        document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');
    }

    function validateCurrentStep() {
        const currentStepEl = document.querySelector(`.form-step[data-step="${currentStep}"]`);
        const inputs = currentStepEl.querySelectorAll('input[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value) {
                isValid = false;
                showInputError(input, 'This field is required');
            } else if (input.type === 'number') {
                const value = parseFloat(input.value);
                if (value < input.min || value > input.max) {
                    isValid = false;
                    showInputError(input, `Please enter a value between ${input.min} and ${input.max}`);
                } else {
                    clearInputError(input);
                }
            } else {
                clearInputError(input);
            }
        });

        return isValid;
    }

    function showInputError(input, message) {
        const errorDiv = input.parentElement.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        input.classList.add('error');
    }

    function clearInputError(input) {
        const errorDiv = input.parentElement.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.textContent = '';
            errorDiv.style.display = 'none';
        }
        input.classList.remove('error');
    }

    function addBotMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${message}</p>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getStepMessage(step) {
        const messages = {
            1: "Great! Now, let's know your weight.",
            2: "Perfect! What's your height?",
            3: "Thanks! What's your gender?",
            4: "Got it! How active are you on a daily basis?",
            5: "Nice! What's your main goal?",
            6: "Almost there! What's your dietary preference?",
            7: "Perfect! Let me generate your personalized diet plan."
        };
        return messages[step] || "";
    }

    function showNotification(message, type = 'success', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notificationArea.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, duration);
    }
}); 