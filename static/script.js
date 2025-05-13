// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Handle auto-fill button click
    const autoFillButton = document.getElementById('auto-fill');
    if (autoFillButton) {
        autoFillButton.addEventListener('click', loadSampleData);
    } else {
        console.error('Auto-fill button not found');
    }

    // Handle form submission
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[type="number"]');
            let allFilled = true;

            inputs.forEach(input => {
                if (!input.value || isNaN(input.value) || input.value < 0) {
                    allFilled = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });

            if (!allFilled) {
                e.preventDefault();
                alert('Please fill all fields with valid positive numbers.');
                console.log('Form submission blocked due to invalid inputs');
            } else {
                console.log('Form submission proceeding');
            }
        });
    } else {
        console.error('Prediction form not found');
    }
});

// Function to load sample data for demonstration
function loadSampleData() {
    // Sample data for the 13 significant features (benign case)
    const sampleData = {
        feature_1: 13.54,   // Radius Mean
        feature_2: 14.36,   // Texture Mean
        feature_3: 87.46,   // Perimeter Mean
        feature_4: 566.3,   // Area Mean
        feature_8: 0.023,   // Concave Points Mean
        feature_13: 2.05,  // Perimeter SE
        feature_14: 23.56,  // Area SE
        feature_15: 0.0051, // Smoothness SE
        feature_21: 15.11,  // Radius Worst
        feature_22: 19.26,  // Texture Worst
        feature_23: 99.7,   // Perimeter Worst
        feature_24: 711.2,  // Area Worst
        feature_28: 0.08    // Concave Points Worst
    };

    // Fill the form with sample data
    Object.keys(sampleData).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            input.value = sampleData[key];
        } else {
            console.error(`Input with ID ${key} not found`);
        }
    });

    // Animate the form to draw attention
    const form = document.getElementById('prediction-form');
    if (form) {
        form.style.transition = 'background-color 0.5s ease';
        form.style.backgroundColor = '#e8f4fc';
        setTimeout(() => {
            form.style.backgroundColor = '#fff';
        }, 1000);
    }
}