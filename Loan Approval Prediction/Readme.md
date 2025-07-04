# Loan Approval Prediction

This machine learning project predicts loan approval decisions based on applicant financial and personal information. The system helps financial institutions automate loan screening by analyzing income, credit history, and demographic factors.

## Project Description

Using supervised learning algorithms, the system evaluates loan applications and predicts approval probability. The model analyzes factors like income, loan amount, credit history, employment status, and property area to make data-driven loan decisions.

## Technical Implementation
- **Algorithms**: Random Forest, Logistic Regression, SVM comparison
- **Features**: 12 applicant attributes including financial and demographic data
- **Target**: Binary classification (Y = approved, N = rejected)
- **Preprocessing**: Missing value imputation and categorical encoding
- **Validation**: Cross-validation and train-test split evaluation

## Model Performance
- **Accuracy**: 83% on test dataset
- **Precision**: 85% for loan approvals
- **Recall**: 82% for identifying approved loans
- **F1-Score**: 83% balanced performance
- **AUC-ROC**: 0.87 area under curve
- **Cross-validation**: 81% average across 5 folds

## Dataset Details
- **Records**: 614 loan applications
- **Features**: 12 attributes (Gender, Married, Dependents, Education, etc.)
- **Target**: Loan_Status (Y/N for approved/rejected)
- **Missing Values**: 10-15% missing data handled with imputation
- **Class Distribution**: 68% approved, 32% rejected

## Installation & Setup
```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

## Usage
```bash
# Open Jupyter notebook
jupyter notebook main.ipynb

# Follow notebook sections:
# 1. Data loading and exploration
# 2. Data preprocessing and cleaning
# 3. Model training and comparison
# 4. Performance evaluation
# 5. Feature importance analysis
```

## Key Features
- **Data Preprocessing**: Automated missing value handling
- **Feature Engineering**: Categorical encoding and scaling
- **Model Comparison**: Multiple algorithms tested
- **Feature Importance**: Analysis of key decision factors
- **Evaluation Metrics**: Comprehensive performance assessment
- **Visualization**: EDA plots and model performance charts

## Applications
- **Banking**: Automated loan screening systems
- **Credit Unions**: Risk assessment and decision support
- **Fintech**: Digital lending platforms
- **Microfinance**: Small loan approval automation
- **Insurance**: Risk evaluation for loan insurance 