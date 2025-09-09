// Wine Quality Prediction System - JavaScript
(function() {
    'use strict';

    // DOM Elements
    const form = document.getElementById('predictionForm');
    const submitBtn = document.querySelector('.predict-btn');
    const resetBtn = document.getElementById('resetForm');
    const inputs = document.querySelectorAll('input[required]');

    // Configuration
    const config = {
        validationRules: {
            fixed_acidity: { min: 0, max: 20, step: 0.01 },
            volatile_acidity: { min: 0, max: 2, step: 0.01 },
            citric_acid: { min: 0, max: 1, step: 0.01 },
            residual_sugar: { min: 0, max: 65, step: 0.01 },
            chlorides: { min: 0, max: 1, step: 0.0001 },
            free_sulfur_dioxide: { min: 0, max: 300, step: 0.1 },
            total_sulfur_dioxide: { min: 0, max: 450, step: 0.1 },
            density: { min: 0.9, max: 1.1, step: 0.0001 },
            pH: { min: 0, max: 14, step: 0.01 },
            sulphates: { min: 0, max: 2, step: 0.01 },
            alcohol: { min: 0, max: 20, step: 0.01 }
        },
        sampleData: {
            fixed_acidity: 7.4,
            volatile_acidity: 0.7,
            citric_acid: 0.0,
            residual_sugar: 1.9,
            chlorides: 0.076,
            free_sulfur_dioxide: 11.0,
            total_sulfur_dioxide: 34.0,
            density: 0.9978,
            pH: 3.51,
            sulphates: 0.56,
            alcohol: 9.4
        }
    };

    // Initialize application
    function init() {
        setupEventListeners();
        setupValidation();
        setupTooltips();
        setupAccessibility();
        console.log('Wine Quality Prediction System initialized');
    }

    // Event Listeners
    function setupEventListeners() {
        // Form submission
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
        }

        // Reset button
        if (resetBtn) {
            resetBtn.addEventListener('click', handleFormReset);
        }

        // Input validation
        inputs.forEach(input => {
            input.addEventListener('blur', validateInput);
            input.addEventListener('input', debounce(validateInput, 300));
            input.addEventListener('focus', clearInputError);
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', handleKeyboardShortcuts);

        // Page visibility
        document.addEventListener('visibilitychange', handleVisibilityChange);
    }

    // Form submission handler
    function handleFormSubmit(e) {
        e.preventDefault();
        
        if (!validateAllInputs()) {
            showAlert('Please correct the errors in the form', 'error');
            return;
        }

        showLoadingState(true);
        
        // Simulate processing time for better UX
        setTimeout(() => {
            form.submit();
        }, 500);
    }

    // Form reset handler
    function handleFormReset() {
        if (confirm('Are you sure you want to reset all fields?')) {
            form.reset();
            clearAllErrors();
            showAlert('Form has been reset', 'success');
        }
    }

    // Loading state management
    function showLoadingState(show) {
        const btnText = submitBtn.querySelector('.btn-text');
        const spinner = submitBtn.querySelector('.spinner-border');
        
        if (show) {
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            btnText.textContent = 'Analyzing...';
            spinner.classList.remove('d-none');
            
            // Show loading overlay
            showLoadingOverlay();
        } else {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
            btnText.textContent = 'Predict Wine Quality';
            spinner.classList.add('d-none');
            
            // Hide loading overlay
            hideLoadingOverlay();
        }
    }

    // Loading overlay
    function showLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="text-center text-white">
                <div class="loading-spinner"></div>
                <p class="mt-3 fs-5">Analyzing wine characteristics...</p>
                <small>This may take a few seconds</small>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    function hideLoadingOverlay() {
        const overlay = document.querySelector('.loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }

    // Input validation
    function validateInput(e) {
        const input = e.target;
        const value = parseFloat(input.value);
        const rules = config.validationRules[input.name];
        
        if (!rules) return;

        let isValid = true;
        let errorMessage = '';

        // Check if value exists
        if (input.value === '' || isNaN(value)) {
            isValid = false;
            errorMessage = 'This field is required';
        }
        // Check range
        else if (value < rules.min || value > rules.max) {
            isValid = false;
            errorMessage = `Value must be between ${rules.min} and ${rules.max}`;
        }

        // Update input state
        if (isValid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            hideInputError(input);
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            showInputError(input, errorMessage);
        }

        return isValid;
    }

    // Validate all inputs
    function validateAllInputs() {
        let allValid = true;
        
        inputs.forEach(input => {
            const event = { target: input };
            if (!validateInput(event)) {
                allValid = false;
            }
        });
        
        return allValid;
    }

    // Error handling
    function showInputError(input, message) {
        const feedback = input.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
        }
    }

    function hideInputError(input) {
        const feedback = input.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = '';
        }
    }

    function clearInputError(e) {
        const input = e.target;
        input.classList.remove('is-invalid');
        hideInputError(input);
    }

    function clearAllErrors() {
        inputs.forEach(input => {
            input.classList.remove('is-invalid', 'is-valid');
            hideInputError(input);
        });
    }

    // Alert system
    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.card-body');
        const form = document.getElementById('predictionForm');
        container.insertBefore(alertDiv, form);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    function getAlertIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // Accessibility setup
    function setupAccessibility() {
        // Add ARIA labels
        inputs.forEach(input => {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (label) {
                input.setAttribute('aria-describedby', `${input.id}-help`);
            }
        });

        // Focus management
        const firstInput = document.querySelector('input');
        if (firstInput) {
            firstInput.focus();
        }
    }

    // Tooltip setup
    function setupTooltips() {
        // Add helpful tooltips to inputs
        const tooltips = {
            fixed_acidity: 'Most acids involved with wine or fixed or nonvolatile (do not evaporate readily)',
            volatile_acidity: 'The amount of acetic acid in wine, which at too high of levels can lead to an unpleasant, vinegar taste',
            citric_acid: 'Found in small quantities, citric acid can add freshness and flavor to wines',
            residual_sugar: 'The amount of sugar remaining after fermentation stops',
            chlorides: 'The amount of salt in the wine',
            free_sulfur_dioxide: 'The free form of SO2 exists in equilibrium between molecular SO2',
            total_sulfur_dioxide: 'Amount of free and bound forms of S02',
            density: 'The density of water is close to that of water depending on the percent alcohol and sugar content',
            pH: 'Describes how acidic or basic a wine is on a scale from 0 (very acidic) to 14 (very basic)',
            sulphates: 'A wine additive which can contribute to sulfur dioxide gas (S02) levels',
            alcohol: 'The percent alcohol content of the wine'
        };

        Object.keys(tooltips).forEach(key => {
            const input = document.getElementById(key);
            if (input) {
                input.setAttribute('title', tooltips[key]);
                input.setAttribute('data-bs-toggle', 'tooltip');
                input.setAttribute('data-bs-placement', 'top');
            }
        });

        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Keyboard shortcuts
    function handleKeyboardShortcuts(e) {
        // Ctrl + Enter to submit
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            if (submitBtn && !submitBtn.disabled) {
                handleFormSubmit(e);
            }
        }
        
        // Ctrl + R to reset (prevent default browser refresh)
        if (e.ctrlKey && e.key === 'r') {
            e.preventDefault();
            handleFormReset();
        }

        // Fill sample data (Ctrl + S)
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            fillSampleData();
        }
    }

    // Fill with sample data
    function fillSampleData() {
        if (confirm('Fill form with sample wine data?')) {
            Object.keys(config.sampleData).forEach(key => {
                const input = document.getElementById(key);
                if (input) {
                    input.value = config.sampleData[key];
                    const event = { target: input };
                    validateInput(event);
                }
            });
            showAlert('Form filled with sample data', 'success');
        }
    }

    // Page visibility handler
    function handleVisibilityChange() {
        if (document.visibilityState === 'visible') {
            // Re-focus first invalid input if any
            const firstInvalid = document.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.focus();
            }
        }
    }

    // Utility functions
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Enhanced validation setup
    function setupValidation() {
        // Add pattern attributes for better HTML5 validation
        inputs.forEach(input => {
            const rules = config.validationRules[input.name];
            if (rules) {
                input.setAttribute('min', rules.min);
                input.setAttribute('max', rules.max);
                input.setAttribute('step', rules.step);
            }
        });

        // Custom validation messages
        form.addEventListener('invalid', function(e) {
            e.preventDefault();
            const firstInvalid = form.querySelector(':invalid');
            if (firstInvalid) {
                firstInvalid.focus();
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }, true);
    }

    // Error recovery
    window.addEventListener('error', function(e) {
        console.error('JavaScript error:', e.error);
        showAlert('An unexpected error occurred. Please refresh the page.', 'error');
        showLoadingState(false);
    });

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export functions for testing (if needed)
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = {
            validateInput,
            validateAllInputs,
            showAlert,
            fillSampleData
        };
    }

})();