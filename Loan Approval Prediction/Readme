# Loan Approval Prediction

This project aims to predict loan approval using machine learning models. It involves data exploration, preprocessing, feature engineering, model training, and evaluation.

## Dataset

The project uses a dataset containing information about loan applicants, including their demographics, financial history, and loan details. The dataset is loaded from a CSV file named 'Dataset.csv'.

## Data Preprocessing

- Missing values are handled by imputing with median for numerical features (LoanAmount, Loan_Amount_Term, Credit_History) and mode for categorical features (Gender, Married, Dependents, Self_Employed).
- Outliers are identified using box plots.
- Categorical features are encoded using Label Encoding.
- Numerical features are scaled using Standard Scaling.

## Feature Engineering

- Total income is calculated by adding applicant income and co-applicant income.
- Log transformation is applied to total income and loan amount to handle skewed distributions.

## Model Training and Evaluation

Several machine learning models are trained and evaluated, including:

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- K-Nearest Neighbors Classifier

The models are evaluated using accuracy and classification report metrics.

## Handling Imbalanced Data

The target variable (Loan_Status) is found to be imbalanced. To address this, SMOTE (Synthetic Minority Over-sampling Technique) is used to oversample the minority class.

## Results

The models' performance is evaluated on the resampled data, and the results are presented in terms of accuracy and classification report.

## Usage

1. Clone the repository.
2. Install the required libraries: `pip install pandas numpy matplotlib seaborn scikit-learn imblearn`.
3. Place the dataset file ('Dataset.csv') in the project directory.
4. Run the Jupyter Notebook to execute the code.


## Conclusion

This project demonstrates the process of building a loan approval prediction model using machine learning. It highlights the importance of data preprocessing, feature engineering, and handling imbalanced data for achieving better model performance.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
