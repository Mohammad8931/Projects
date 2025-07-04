# House Price Prediction Website

This full-stack web application predicts house prices in Bangalore using machine learning. Users can input property details through a web interface and get instant price predictions based on location, size, and amenities.

## Project Description

A complete real estate price prediction system with HTML/CSS/JavaScript frontend and Flask backend. The system uses linear regression trained on Bangalore housing data to provide accurate price estimates based on area, location, bedrooms, and bathrooms.

## Technical Implementation
- **Frontend**: HTML5, CSS3, JavaScript with responsive design
- **Backend**: Flask web framework with RESTful API
- **Model**: Linear Regression for price prediction
- **Data**: Bangalore house prices dataset with feature engineering
- **Deployment**: Ready for cloud deployment (Heroku, AWS, etc.)

## Model Performance
- **R² Score**: 84% variance explained
- **Mean Absolute Error**: ₹12 lakhs average prediction error
- **Training Accuracy**: 85%+ on validation set
- **Features**: 4 key inputs (location, sqft, bedrooms, bathrooms)
- **Locations**: 240+ Bangalore areas supported

## Dataset Details
- **Source**: Bangalore house sales data
- **Samples**: 13,000+ property records
- **Features**: Area (sqft), location, BHK configuration, bathrooms
- **Price Range**: ₹8 lakhs to ₹12 crores
- **Data Cleaning**: Outlier removal and feature standardization

## Installation & Setup
```bash
# Backend setup
cd server
pip install flask pandas numpy scikit-learn

# Run Flask server
python server.py

# Frontend setup
cd client
# Open app.html in browser or serve via HTTP server
```

## Usage
```bash
# Start the server
cd server
python server.py

# Open web application
# Navigate to client/app.html in browser

# Enter details:
# - Select location from dropdown
# - Input area in square feet
# - Choose number of bedrooms
# - Choose number of bathrooms
# - Click "Estimate Price"
```

## Key Features
- **Interactive Web UI**: Clean, responsive design with form validation
- **Real-time Predictions**: Instant price estimates via AJAX
- **Location Dropdown**: 240+ Bangalore areas with autocomplete
- **Input Validation**: Client and server-side data validation
- **Price Formatting**: Currency formatting with lakhs/crores display
- **Mobile Responsive**: Works on desktop and mobile devices

## File Structure
```
House Price Prediction Website/
├── client/                  # Frontend application
│   ├── app.html            # Main web interface
│   ├── app.css             # Styling and layout
│   ├── app.js              # Frontend JavaScript logic
│   └── house.PNG           # UI graphics
├── server/                  # Backend API
│   ├── server.py           # Flask application
│   ├── util.py             # Utility functions
│   └── artifacts/          # Model and data files
│       ├── banglore_home_prices_model.pickle
│       └── columns.json
├── model/                   # ML development
│   ├── Price Prediction.ipynb
│   ├── Bengaluru_House_Data.csv
│   └── columns.json
└── README.md               # Documentation
```

## API Endpoints
```python
GET /get_location_names     # Fetch available locations
POST /predict_home_price    # Get price prediction
```

## Web Interface Features
- **Location Selection**: Dropdown with all Bangalore areas
- **Area Input**: Square feet with validation (300-10000 sqft)
- **BHK Selection**: Bedrooms (1-5) with radio buttons
- **Bathroom Selection**: Bathrooms (1-5) with radio buttons
- **Price Display**: Formatted result in lakhs/crores

## Prediction Logic
```python
def predict_price(location, sqft, bath, bhk):
    # Load model and columns
    model = pickle.load(open('model.pickle', 'rb'))
    columns = json.load(open('columns.json', 'r'))
    
    # Create feature vector
    x = np.zeros(len(columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    
    # Set location feature
    if location in columns:
        loc_index = columns.index(location)
        x[loc_index] = 1
    
    return model.predict([x])[0]
```

## Data Processing
- **Outlier Removal**: Properties with unusual size/price ratios
- **Feature Engineering**: Per sqft price analysis and location encoding
- **Standardization**: Area normalization and categorical encoding
- **Train/Test Split**: 80/20 split for model validation

## Applications
- **Real Estate**: Property valuation and investment decisions
- **Home Buyers**: Budget planning and price comparison
- **Agents**: Quick price estimates for clients
- **Developers**: Market analysis and pricing strategy
- **Research**: Housing market trend analysis

## Model Features
**Input Parameters:**
- **Location**: 240+ Bangalore areas (Whitefield, Koramangala, etc.)
- **Total Square Feet**: Property area (300-10000 sqft)
- **Bedrooms**: Number of bedrooms (1-5 BHK)
- **Bathrooms**: Number of bathrooms (1-5)

## UI Screenshots
The interface includes a clean form with:
- Location dropdown with search functionality
- Area input with validation
- BHK and bathroom selection buttons
- Real-time price prediction display
- Mobile-responsive design

## Deployment Notes
- **Flask Development**: Built-in development server
- **Production**: Use Gunicorn or uWSGI for production
- **Cloud**: Ready for Heroku, AWS, or Google Cloud deployment
- **Database**: Can be extended with PostgreSQL for user data 