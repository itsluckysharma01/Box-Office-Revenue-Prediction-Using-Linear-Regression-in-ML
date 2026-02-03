# 🎬 Box Office Revenue Prediction Using Machine Learning

An **interactive Flask web application** that predicts movie box office revenue using an **XGBoost regression model** trained on historical movie data. This project combines machine learning with a beautiful, responsive web interface to provide instant revenue predictions for movies.

## ✨ Features

### 🎨 Interactive Web Interface

- **Modern UI Design**: Beautiful gradient backgrounds with smooth animations
- **Real-time Validation**: Input fields validate as you type with visual feedback
- **Live Counters**: See theater counts and genre selections update in real-time
- **Tooltips**: Helpful information on hover for each input field
- **Responsive Design**: Perfectly adapts to desktop, tablet, and mobile devices

### 🤖 Machine Learning Powered

- **XGBoost Algorithm**: State-of-the-art gradient boosting model
- **Multiple Features**: Analyzes distributor, MPAA rating, theaters, genres, and more
- **Fast Predictions**: Instant results with detailed breakdowns
- **Log-Scale Processing**: Handles large revenue ranges effectively

### 📊 Input Parameters

- 🎥 **Movie Title**: Name of the film
- 🏢 **Distributor**: Studio distributing the movie (Warner Bros., Universal, etc.)
- 📋 **MPAA Rating**: Content rating (G, PG, PG-13, R, NC-17, Not Rated)
- 🎪 **Opening Theaters**: Number of theaters for opening weekend
- 📅 **Release Days**: Expected theatrical run duration
- 🎭 **Genres**: Multi-select from 17 different genres

### 📈 Results Display

- 💰 **Revenue Prediction**: Displayed in both full format and millions
- 📊 **Visual Comparisons**: Bar charts comparing to industry benchmarks
- 🎬 **Movie Details**: Organized card layout with all input parameters
- 🏆 **Genre Badges**: Beautiful display of selected genres
- ⚠️ **Disclaimer**: Important notes about prediction accuracy

## 🧠 Model Performance

| Metric                     | Value                                                 |
| -------------------------- | ----------------------------------------------------- |
| **Algorithm**              | XGBoost Regressor                                     |
| **Training Error (MAE)**   | 0.21                                                  |
| **Validation Error (MAE)** | 0.63                                                  |
| **Features Used**          | 20+ features including genres, theaters, release days |
| **Data Transformation**    | Log10 scaling for revenue and numeric features        |

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **Git** (optional, for cloning)

### Option 1: Easy Run (Windows)

Simply double-click `run.bat` file - it will automatically:

1. Create a virtual environment
2. Install all dependencies
3. Start the Flask server
4. Open at http://localhost:5000

### Option 2: Manual Installation

1. **Navigate to project directory**

   ```bash
   cd Box_Office_Revenue_Prediction_Using_Linear_Regression_in_ML
   ```

2. **Create virtual environment (recommended)**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model files exist**

   Ensure these files are in the project root:
   - ✅ `box_office_model_joblib.pkl`
   - ✅ `scaler.pkl`

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Open your browser**

   Navigate to: **http://localhost:5000**

## 📁 Project Structure

```
Box_Office_Revenue_Prediction/
│
├── app.py                          # Flask application main file
├── requirements.txt                # Python dependencies
├── run.bat                         # Windows quick start script
├── run.sh                          # Linux/Mac quick start script
│
├── box_office_model_joblib.pkl    # Trained XGBoost model
├── scaler.pkl                      # StandardScaler for features
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Styles with animations
│   └── js/
│       └── script.js              # Interactive JavaScript
│
├── templates/                      # HTML templates
│   ├── index.html                 # Main prediction form
│   └── result.html                # Results display page
│
└── Box_Office_Revenue_Prediction_Using_Linear_Regression_in_ML.ipynb
                                    # Jupyter notebook with model training
```

```python
joblib.dump(scaler, 'scaler.pkl')
```

### Running the Application

1. **Start the Flask server**

   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:

   ```
   http://localhost:5000
   ```

3. **Enter movie details** and click "Predict Revenue" to get predictions!

## 📁 Project Structure

```
Box_Office_Revenue_Prediction_Using_Linear_Regression_in_ML/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── box_office_model_joblib.pkl     # Trained XGBoost model
├── scaler.pkl                      # Feature scaler
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       └── script.js              # JavaScript functionality
├── templates/
│   ├── index.html                 # Home page with prediction form
│   └── result.html                # Results display page
└── Box_Office_Revenue_Prediction_Using_Linear_Regression_in_ML.ipynb
```

## 🔧 API Usage

### POST /api/predict

Make predictions programmatically using the REST API:

**Request:**

```json
{
  "opening_theaters": 3000,
  "release_days": 120,
  "distributor": 0,
  "mpaa": 2
}
```

**Response:**

```json
{
  "success": true,
  "predicted_revenue": 123456789.0,
  "formatted_revenue": "$123,456,789.00"
}
```

## 📝 Model Details

The prediction model was trained on historical box office data with the following features:

- **Distributor**: Major film distributors (Warner Bros., Universal, etc.)
- **MPAA Rating**: Movie content ratings (G, PG, PG-13, R, NC-17)
- **Opening Theaters**: Number of theaters on opening weekend
- **Release Days**: Total theatrical release duration
- **Genres**: Multiple genre classification (Action, Comedy, Drama, etc.)

### Data Preprocessing

1. Log transformation applied to numeric features
2. One-hot encoding for genres
3. Label encoding for categorical variables
4. Standard scaling for feature normalization

## 🎨 UI Features

- **Gradient Background**: Eye-catching purple gradient
- **Form Validation**: Real-time input validation
- **Genre Selection**: Multi-select checkbox interface
- **Loading States**: Visual feedback during predictions
- **Responsive Layout**: Mobile-first design
- **Smooth Animations**: Enhanced user experience
- **Keyboard Shortcuts**: Ctrl/Cmd + Enter to submit

## 🔮 Future Enhancements

- [ ] Add more features (marketing budget, star power, etc.)
- [ ] Implement model comparison (Linear Regression vs XGBoost)
- [ ] Add historical data visualization
- [ ] Include confidence intervals
- [ ] Export predictions to PDF/CSV
- [ ] User authentication for prediction history
- [ ] A/B testing different models

## 📊 Technology Stack

- **Backend**: Flask (Python)
- **ML Framework**: XGBoost, Scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas, NumPy
- **Model Persistence**: Joblib

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a demonstration of machine learning model deployment using Flask.

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**Note**: Predictions are based on historical data and should be used for informational purposes only. Actual box office revenue may vary significantly based on numerous factors not captured in the model.
