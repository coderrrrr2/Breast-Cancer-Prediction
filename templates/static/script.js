// JavaScript for Breast Cancer Prediction System

document.addEventListener('DOMContentLoaded', function() {
    // Handle sample data button click
    const sampleDataButton = document.getElementById('sample-data');
    if (sampleDataButton) {
        sampleDataButton.addEventListener('click', loadSampleData);
    }
    
    // Handle form submission
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[type="number"]');
            let allFilled = true;
            
            inputs.forEach(input => {
                if (!input.value) {
                    allFilled = false;
                }
            });
            
            if (!allFilled) {
                e.preventDefault();
                alert('Please fill in all feature values before submitting.');
            }
        });
    }
});

// Function to load sample data for demonstration
function loadSampleData() {
    // Sample data based on a typical malignant case
    // These values are representative of the Wisconsin Breast Cancer dataset
    const sampleData = {
        feature_1: 17.99,  // Radius (mean)
        feature_2: 10.38,  // Texture (mean)
        feature_3: 122.8,  // Perimeter (mean)
        feature_4: 1001.0, // Area (mean)
        feature_5: 0.1184, // Smoothness (mean)
        feature_6: 0.2776, // Compactness (mean)
        feature_7: 0.3001, // Concavity (mean)
        feature_8: 0.1471, // Concave points (mean)
        feature_9: 0.2419, // Symmetry (mean)
        feature_10: 0.07871, // Fractal dimension (mean)
        feature_11: 1.095,   // Radius (SE)
        feature_12: 0.9053,  // Texture (SE)
        feature_13: 8.589,   // Perimeter (SE)
        feature_14: 153.4,   // Area (SE)
        feature_15: 0.006399, // Smoothness (SE)
        feature_16: 0.04904,  // Compactness (SE)
        feature_17: 0.05373,  // Concavity (SE)
        feature_18: 0.01587,  // Concave points (SE)
        feature_19: 0.03003,  // Symmetry (SE)
        feature_20: 0.006193, // Fractal dimension (SE)
        feature_21: 25.38,    // Radius (worst)
        feature_22: 17.33,    // Texture (worst)
        feature_23: 184.6,    // Perimeter (worst)
        feature_24: 2019.0,   // Area (worst)
        feature_25: 0.1622,   // Smoothness (worst)
        feature_26: 0.6656,   // Compactness (worst)
        feature_27: 0.7119,   // Concavity (worst)
        feature_28: 0.2654,   // Concave points (worst)
        feature_29: 0.4601,   // Symmetry (worst)
        feature_30: 0.1189    // Fractal dimension (worst)
    };
    
    // Fill the form with sample data
    Object.keys(sampleData).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            input.value = sampleData[key];
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