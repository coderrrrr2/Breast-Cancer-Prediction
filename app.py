from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import os

app = Flask(__name__)

# Load the model and scaler
model_path = 'svm_model.pkl'
scaler_path = 'scaler.pkl'

# Load model and scaler
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)
    
with open(scaler_path, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get feature values from form
        features = []
        for i in range(1, 31):
            feature_name = f'feature_{i}'
            feature_value = float(request.form.get(feature_name, 0))
            features.append(feature_value)
            
        # Convert to numpy array and reshape
        features_array = np.array(features).reshape(1, -1)
        
        # Scale features
        scaled_features = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(scaled_features)
        probability = model.predict_proba(scaled_features)
        
        # Determine result
        result = "Malignant" if prediction[0] == 1 else "Benign"
        prob_malignant = round(probability[0][1] * 100, 2)
        
        return render_template(
            'result.html', 
            prediction=result, 
            probability=prob_malignant
        )
    
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)