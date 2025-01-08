# AAPL Stock Price Prediction using LSTM

This project implements a time series forecasting model using an LSTM (Long Short-Term Memory) neural network to predict the daily closing prices of Apple Inc. (AAPL) stock. The project follows a complete machine learning pipeline, from data acquisition and preprocessing to model training, prediction, and evaluation.

## Project Overview

The primary goal of this project is to demonstrate the application of LSTM networks for time series forecasting in a financial context. Specifically, the model is trained to predict the next day's closing price of AAPL stock based on a 60-day historical lookback window.

## Methodology

The project follows these key steps:

1.  **Data Acquisition:** Historical AAPL stock data is retrieved from Yahoo Finance using the `yfinance` library, covering the period from January 1, 2015, to January 6, 2025.
2.  **Data Preprocessing:**
    *   The dataset is filtered to only include the "Close" price column.
    *   The `MinMaxScaler` from `scikit-learn` is used to scale the data between 0 and 1. This is crucial for optimizing the performance of neural networks.
3.  **Dataset Preparation:**
    *   The dataset is split into training (80%) and testing (20%) sets.
    *   A 60-day lookback window is used to create the training and testing sequences. This means the model takes the past 60 days' closing prices as input to predict the next day's price.
4.  **Model Building:**
    *   An LSTM model is constructed using the `Keras` API.
    *   The model consists of two LSTM layers (with 50 units each), followed by two dense layers (with 25 and 1 unit, respectively).
5.  **Model Training:**
    *   The model is trained on the training set.
    *   The `Adam` optimizer is used to update the model weights.
    *   The Mean Squared Error (MSE) is used as the loss function.
    * The model is fitted with a batch size of 1 and only 1 epoch, to be faster.
6.  **Model Evaluation:**
    *   The trained model is used to predict the closing prices on the test set.
    *   Predictions are inverse transformed to their original scale.
    *   The model's accuracy is evaluated using the Root Mean Squared Error (RMSE) metric.
7.  **Model usage** the `predict_stock_price(start_date, end_date)` function will be able to use the trained model to predict the closing price for a certain date.

## Libraries Used

*   `yfinance`: For downloading historical stock data from Yahoo Finance.
*   `scikit-learn`: For data preprocessing, specifically `MinMaxScaler`.
*   `Keras`: For building and training the LSTM model.
*   `NumPy`: For numerical computations and array handling.
*   `Matplotlib`: For data visualization and plotting.

## Key Features

*   **LSTM (Long Short-Term Memory):** The core of the prediction model, chosen for its effectiveness in time series analysis.
*   **Time Series Analysis:** The project demonstrates the techniques used to work with sequential data, as well as the important step of dividing data into time windows.
*   **Data Scaling:** The use of `MinMaxScaler` to improve model training.
*   **RMSE Evaluation:**  A standard metric for evaluating the model's accuracy in financial forecasting.
* **One step ahead prediction:** the model is designed to predict only one day after the last 60 days.

## Challenges & Learnings

*   **Time Series Data:** This project presented interesting challenges in working with the sequential nature of time series data.
*   **LSTM Architecture:** The proper construction of the architecture was the hardest part of the project.
*   **Data Preprocessing:** The proper data preparation using `MinMaxScaler` is a key part of the process.
*   **Short-Term vs. Long-Term Predictions:** Gained valuable insights into the limitations of one-step-ahead predictions in stock prices.

## How to Use

1.  **Clone the Repository:**
