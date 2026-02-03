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

# Sample movie titles for autocomplete suggestions
POPULAR_MOVIES = [
    'Avatar', 'Avengers: Endgame', 'Titanic', 'Star Wars: The Force Awakens',
    'Avengers: Infinity War', 'Spider-Man: No Way Home', 'Jurassic World',
    'The Lion King', 'The Avengers', 'Furious 7', 'Frozen II', 'Frozen',
    'Black Panther', 'Harry Potter and the Deathly Hallows Part 2',
    'Star Wars: The Last Jedi', 'Jurassic World: Fallen Kingdom',
    'Beauty and the Beast', 'Incredibles 2', 'The Fate of the Furious',
    'Iron Man 3', 'Minions', 'Captain America: Civil War', 'Aquaman',
    'The Dark Knight', 'Toy Story 4', 'Toy Story 3', 'Wonder Woman',
    'Iron Man', 'Captain Marvel', 'Transformers: Dark of the Moon',
    'Skyfall', 'Transformers: Age of Extinction', 'The Dark Knight Rises',
    'Joker', 'Star Wars: The Rise of Skywalker', 'Finding Dory',
    'Star Wars: Episode I', 'Alice in Wonderland', 'Zootopia',
    'The Hobbit: An Unexpected Journey', 'The Hunger Games: Catching Fire',
    'Pirates of the Caribbean: Dead Mans Chest', 'Rogue One',
    'Aladdin', 'Bohemian Rhapsody', 'Despicable Me 3', 'Jumanji',
    'The Jungle Book', 'Pirates of the Caribbean: On Stranger Tides',
    'Deadpool', 'Inside Out', 'Guardians of the Galaxy Vol. 2',
    'Spider-Man: Far From Home', 'Captain America: The Winter Soldier',
    'The Secret Life of Pets', 'Batman v Superman', 'Guardians of the Galaxy',
    'Maleficent', 'Spider-Man', 'Thor: Ragnarok', 'Venom', 'The Matrix',
    'Inception', 'Interstellar', 'Forrest Gump', 'The Shawshank Redemption',
    'Pulp Fiction', 'The Godfather', 'The Lord of the Rings',
    'Back to the Future', 'Gladiator', 'Jurassic Park', 'E.T.',
    'Finding Nemo', 'Shrek 2', 'Up', 'WALL-E', 'Ratatouille', 'Moana',
    'Coco', 'Brave', 'Tangled', 'Big Hero 6', 'Wreck-It Ralph',
    'How to Train Your Dragon', 'Kung Fu Panda', 'Madagascar',
    'The Incredibles', 'Monsters Inc', 'Cars', 'A Bugs Life',
    'The Good Dinosaur', 'Onward', 'Soul', 'Luca', 'Turning Red', 'Encanto'
]

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

@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    """API endpoint to search for movie suggestions"""
    query = request.args.get('q', '').lower()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    # Filter movies that match the query
    suggestions = [movie for movie in POPULAR_MOVIES if query in movie.lower()]
    
    # Return top 10 matches
    return jsonify(suggestions[:10])

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