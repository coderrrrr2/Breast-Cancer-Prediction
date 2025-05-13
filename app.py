from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import os
import logging
import joblib  

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.environ.get('MODEL_PATH', os.path.join(BASE_DIR, 'svm_model.pkl'))
scaler_path = os.environ.get('SCALER_PATH', os.path.join(BASE_DIR, 'scaler.pkl'))


model = None
scaler = None
model_loaded = False

def load_model():
    """Load the model and scaler using joblib."""
    global model, scaler, model_loaded  # Add model_loaded here
    try:
        logger.info(f"Loading model from: {model_path}")
        model = joblib.load(model_path)

        logger.info(f"Loading scaler from: {scaler_path}")
        scaler = joblib.load(scaler_path)

        model_loaded = True  # ✅ This is key
        logger.info("Model and scaler loaded successfully")
        return True
    except FileNotFoundError as e:
        logger.error(f"Model or scaler file not found: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to load model or scaler: {str(e)}")
        return False





load_model()

@app.route('/')
def home():
    """Render the home page."""
    logger.info(f"Model loaded on home route: {model_loaded}")
    return render_template('index.html', model_loaded=model_loaded)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request for 13 features."""
    if not model_loaded:
        logger.error("Model not loaded at prediction time")
        return render_template('error.html', error="Model not loaded")

    try:
        logger.info(f"Received form data: {request.form}")
        
        # Define the 13 features to collect (1-based form indices)
        feature_indices = [1, 2, 3, 4, 8, 13, 14, 15, 21, 22, 23, 24, 28]
        features = []
        
        for i in feature_indices:
            feature_name = f'feature_{i}'
            feature_value = request.form.get(feature_name)
            if not feature_value:
                logger.error(f"Missing value for {feature_name}")
                return render_template('error.html', error=f"Missing value for {feature_name}")
            try:
                val = float(feature_value)
                if val < 0:
                    logger.error(f"Negative value for {feature_name}: {val}")
                    return render_template('error.html', error=f"Value for {feature_name} must be positive")
                features.append(val)
            except ValueError:
                logger.error(f"Invalid float for {feature_name}: {feature_value}")
                return render_template('error.html', error=f"Invalid value for {feature_name}")

        # Convert to numpy array (13 features)
        features_array = np.array(features).reshape(1, -1)
        logger.info(f"Features array: {features_array}")
        
        # Scale features (scaler expects 13 features)
        scaled_features = scaler.transform(features_array)
        logger.info(f"Scaled features: {scaled_features}")
        
        # Make prediction
        prediction = model.predict(scaled_features)
        probability = model.predict_proba(scaled_features)
        logger.info(f"Prediction: {prediction}, Probability: {probability}")

        # Determine result
        result = "Malignant" if prediction[0] == 1 else "Benign"
        prob_malignant = round(probability[0][1] * 100, 2)

        return render_template('result.html', prediction=result, probability=prob_malignant)

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/upload', methods=['GET', 'POST'])
def upload_model():
    """Handle model upload and reload."""
    global model_loaded
    if request.method == 'POST':
        try:
            if 'model_file' not in request.files or 'scaler_file' not in request.files:
                return render_template('index.html', error="Both model and scaler files are required")

            model_file = request.files['model_file']
            scaler_file = request.files['scaler_file']

            if model_file.filename == '' or scaler_file.filename == '':
                return render_template('index.html', error="No file selected")

            model_file.save(model_path)
            scaler_file.save(scaler_path)

            model_loaded = load_model()

            if model_loaded:
                return render_template('index.html', success="Model and scaler uploaded successfully")
            else:
                return render_template('index.html', error="Failed to load the uploaded files")

        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return render_template('index.html', error=str(e))

    return render_template('index.html', model_loaded=model_loaded)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5450))
    app.run(host='0.0.0.0', port=port, debug=True)
