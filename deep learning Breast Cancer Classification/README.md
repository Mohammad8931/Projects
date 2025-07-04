# Breast Cancer Classification

This deep learning project classifies breast cancer as benign or malignant using neural networks. The system analyzes medical diagnostic features to help with early cancer detection and medical decision support.

## Project Description

The model uses the Wisconsin Breast Cancer dataset containing 30 diagnostic features extracted from digitized images of breast mass cell nuclei. It implements a neural network to distinguish between benign and malignant cases with high accuracy.

## Technical Implementation
- **Model Architecture**: Multi-layer neural network with dense layers
- **Input Features**: 30 numerical measurements (mean radius, texture, perimeter, area, etc.)
- **Output**: Binary classification (0 = malignant, 1 = benign)
- **Framework**: TensorFlow/Keras
- **Data Preprocessing**: StandardScaler normalization

## Dataset Details
- **Total Samples**: 569 breast cancer cases
- **Features**: 30 diagnostic measurements
- **Classes**: Benign (357 cases) vs Malignant (212 cases)
- **Data Split**: 80% training, 20% testing with stratification
- **Source**: Wisconsin Breast Cancer Database

## Model Performance
- **Training Accuracy**: 99%+
- **Validation Accuracy**: 95%+
- **Test Accuracy**: 93%+
- **Training Time**: ~100 epochs
- **Model Size**: Lightweight for deployment

## Installation & Setup
```bash
pip install tensorflow pandas numpy scikit-learn matplotlib seaborn
```

## Usage
```bash
# Open Jupyter notebook
jupyter notebook main.ipynb

# Run cells to:
# 1. Load and explore dataset
# 2. Preprocess data
# 3. Train neural network
# 4. Evaluate performance
# 5. Make predictions
```

## Key Features
- **Data Preprocessing**: StandardScaler for feature normalization
- **Model Architecture**: Sequential neural network with multiple layers
- **Performance Metrics**: Comprehensive evaluation with accuracy, precision, recall
- **Visualization**: Training history and performance plots
- **Medical Focus**: Designed for healthcare applications

## File Structure
```
├── main.ipynb    # Complete analysis and model training
└── README.md     # Project documentation
```

## Applications
- **Medical Diagnosis**: Supporting cancer detection decisions
- **Healthcare AI**: Automated screening systems
- **Research**: Understanding diagnostic feature importance
- **Education**: Learning medical AI applications

## Model Architecture
```python
model = Sequential([
    Flatten(input_shape=(30,)),
    Dense(20, activation='relu'),
    Dense(2, activation='sigmoid')
])
```

## Important Note
This model is for educational and research purposes only. It should never replace professional medical evaluation or be used as the sole basis for medical decisions. 