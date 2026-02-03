from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
import pickle

app = Flask(__name__)

# Load the trained model
model = joblib.load('box_office_model_joblib.pkl')

# Load the scaler (you'll need to save this from your notebook)
try:
    scaler = joblib.load('scaler.pkl')
except:
    scaler = StandardScaler()
    print("Warning: Scaler not found. Using default scaler.")

# Define MPAA and distributor mappings (based on common values)
MPAA_OPTIONS = ['G', 'PG', 'PG-13', 'R', 'NC-17', 'Not Rated']
DISTRIBUTOR_OPTIONS = [
    'Warner Bros.', 'Universal', 'Paramount Pictures', 'Walt Disney Studios',
    '20th Century Fox', 'Sony Pictures', 'Lionsgate', 'MGM', 'Others'
]

# Genre options - Only the genres that were actually used in training
GENRE_OPTIONS = ['action', 'animation', 'comedy', 'drama', 'horror', 'thriller']

# These are the exact feature columns used during model training (in order)
FEATURE_COLUMNS = ['distributor', 'opening_theaters', 'MPAA', 'release_days', 
                   'action', 'animation', 'comedy', 'drama', 'horror', 'thriller']

@app.route('/')
def home():
    return render_template('index.html', 
                         mpaa_options=MPAA_OPTIONS,
                         distributor_options=DISTRIBUTOR_OPTIONS,
                         genre_options=GENRE_OPTIONS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        title = request.form.get('title', 'Unknown Movie')
        distributor = request.form.get('distributor')
        mpaa = request.form.get('mpaa')
        opening_theaters = float(request.form.get('opening_theaters'))
        release_days = float(request.form.get('release_days'))
        
        # Get selected genres
        genres = request.form.getlist('genres')
        
        # Apply log transformation (as done in the notebook)
        opening_theaters_log = np.log10(opening_theaters) if opening_theaters > 0 else 0
        release_days_log = np.log10(release_days) if release_days > 0 else 0
        
        # Encode categorical variables
        distributor_mapping = {dist: idx for idx, dist in enumerate(DISTRIBUTOR_OPTIONS)}
        mpaa_mapping = {rating: idx for idx, rating in enumerate(MPAA_OPTIONS)}
        
        # Create feature dictionary with exact columns in the correct order
        features_dict = {
            'distributor': distributor_mapping.get(distributor, 0),
            'opening_theaters': opening_theaters_log,
            'MPAA': mpaa_mapping.get(mpaa, 0),
            'release_days': release_days_log,
            'action': 1 if 'action' in genres else 0,
            'animation': 1 if 'animation' in genres else 0,
            'comedy': 1 if 'comedy' in genres else 0,
            'drama': 1 if 'drama' in genres else 0,
            'horror': 1 if 'horror' in genres else 0,
            'thriller': 1 if 'thriller' in genres else 0
        }
        
        # Create DataFrame with features in correct order
        input_df = pd.DataFrame([features_dict], columns=FEATURE_COLUMNS)
        
        # Scale features
        input_scaled = scaler.transform(input_df)
        
        # Make prediction (log scale)
        prediction_log = model.predict(input_scaled)[0]
        
        # Convert back from log scale
        prediction = 10 ** prediction_log
        
        # Format the prediction
        prediction_formatted = f"${prediction:,.2f}"
        prediction_millions = f"${prediction/1_000_000:.2f}M"
        
        return render_template('result.html',
                             title=title,
                             prediction=prediction_formatted,
                             prediction_millions=prediction_millions,
                             opening_theaters=int(opening_theaters),
                             release_days=int(release_days),
                             mpaa=mpaa,
                             distributor=distributor,
                             genres=', '.join(genres) if genres else 'None')
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Error:", error_details)  # Print to console for debugging
        return render_template('result.html',
                             error=f"An error occurred: {str(e)}",
                             title=request.form.get('title', 'Unknown'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        # Extract features
        opening_theaters = float(data.get('opening_theaters', 0))
        release_days = float(data.get('release_days', 0))
        
        # Apply log transformation
        opening_theaters_log = np.log10(opening_theaters) if opening_theaters > 0 else 0
        release_days_log = np.log10(release_days) if release_days > 0 else 0
        
        # Create feature array (adjust based on your model's requirements)
        features = np.array([[
            data.get('distributor', 0),
            data.get('mpaa', 0),
            opening_theaters_log,
            release_days_log
        ]])
        
        # Make prediction
        prediction_log = model.predict(features)[0]
        prediction = 10 ** prediction_log
        
        return jsonify({
            'success': True,
            'predicted_revenue': float(prediction),
            'formatted_revenue': f"${prediction:,.2f}"
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)